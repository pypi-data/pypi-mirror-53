# Copyright (c) 2004-2019 mudpy authors. Permission to use, copy,
# modify, and distribute this software is granted under terms
# provided in the LICENSE file distributed with this software.

import os
import pathlib
import re
import shutil
import subprocess
import sys
import telnetlib
import time

pidfile = "var/mudpy.pid"

test_account0_setup = (
    (0, "Identify yourself:", "luser0"),
    (0, "Enter your choice:", "n"),
    (0, 'Enter a new password for "luser0":', "Test123"),
    (0, "Enter the same new password again:", "Test123"),
    (0, r"What would you like to do\?", "c"),
    (0, "Pick a birth gender for your new avatar:", "f"),
    (0, "Choose a name for her:", "1"),
    (0, "What would you like to do?", "a"),
    (0, "Whom would you like to awaken?", ""),
)

test_account1_setup = (
    (1, "Identify yourself:", "luser1"),
    (1, "Enter your choice:", "n"),
    (1, 'Enter a new password for "luser1":', "Test456"),
    (1, "Enter the same new password again:", "Test456"),
    (1, r"What would you like to do\?", "c"),
    (1, "Pick a birth gender for your new avatar:", "m"),
    (1, "Choose a name for him:", "1"),
    (1, "What would you like to do?", "a"),
    (1, "Whom would you like to awaken?", ""),
)

test_actor_appears = (
    (0, r"You suddenly realize that .* is here\.", ""),
)

test_explicit_punctuation = (
    (0, "> ", "say Hello there!"),
    (0, r'You exclaim, "Hello there\!"', ""),
    (1, r'exclaims, "Hello there\!"', "say And you are?"),
    (1, r'You ask, "And you are\?"', ""),
    (0, r'asks, "And you are\?"', "say I'm me, of course."),
    (0, r'''You say, "I'm me, of course\."''', ""),
    (1, r'''says, "I'm me, of course\."''', "say I wouldn't be so sure..."),
    (1, r'''You muse, "I wouldn't be so sure\.\.\."''', ""),
    (0, r'''muses, "I wouldn't be so sure\.\.\."''', "say You mean,"),
    (0, 'You begin, "You mean,"', ""),
    (1, 'begins, "You mean,"', "say I know-"),
    (1, 'You begin, "I know-"', ""),
    (0, 'begins, "I know-"', "say Don't interrupt:"),
    (0, r'''You begin, "Don't interrupt:"''', ""),
    (1, r'''begins, "Don't interrupt:"''', "say I wasn't interrupting;"),
    (1, r'''You begin, "I wasn't interrupting;"''', ""),
    (0, r'''begins, "I wasn't interrupting;"''', ""),
)

test_implicit_punctuation = (
    (0, '> ', "say Whatever"),
    (0, r'You say, "Whatever\."', ""),
    (1, r'says, "Whatever\."', ""),
)

test_typo_replacement = (
    (1, '> ', "say That's what i think."),
    (1, r'''You say, "That's what I think\."''', ""),
    (0, r'''says, "That's what I think\."''', "say You know what i'd like."),
    (0, r'''You say, "You know what I'd like\."''', ""),
    (1, r'''says, "You know what I'd like\."''', "say Then i'll tell you."),
    (1, r'''You say, "Then I'll tell you\."''', ""),
    (0, r'''says, "Then I'll tell you\."''', "say Now i'm ready."),
    (0, r'''You say, "Now I'm ready\."''', ""),
    (1, r'''says, "Now I'm ready\."''', "say That's teh idea."),
    (1, r'''You say, "That's the idea\."''', ""),
    (0, r'''says, "That's the idea\."''', "say It's what theyre saying."),
    (0, r'''You say, "It's what they're saying\."''', ""),
    (1, r'''says, "It's what they're saying\."''', "say Well, youre right."),
    (1, r'''You say, "Well, you're right\."''', ""),
    (0, r'''says, "Well, you're right\."''', ""),
)

test_sentence_capitalization = (
    (0, "> ", "say this sentence should start with a capital T."),
    (0, 'You say, "This sentence', ""),
    (1, 'says, "This sentence', ""),
)

test_chat_mode = (
    (1, '> ', "chat"),
    (1, r'(?s)Entering chat mode .*> \(chat\) ', "Feeling chatty."),
    (1, r'You say, "Feeling chatty\."', "!chat"),
    (0, r'says, "Feeling chatty\."', ""),
    (1, '> ', "say Now less chatty."),
    (1, r'You say, "Now less chatty\."', ""),
    (0, r'says, "Now less chatty\."', ""),
)

test_wrapping = (
    (0, '> ', "say " + 100 * "o"),
    (1, r'says,\r\n"O[o]+\."', ""),
)

test_forbid_ansi_input = (
    (0, '> ', "say \x1b[35mfoo\x1b[0m"),
    (1, r'says, "\[35mfoo\[0m\."', ""),
)

test_escape_macros = (
    (0, '> ', "say $(red)bar$(nrm)"),
    (1, r'says, "\$\(red\)bar\$\(nrm\)."', ""),
)

test_movement = (
    (0, "> ", "move north"),
    (0, r"You exit to the north\.", ""),
    (1, r"exits to the north\.", "move north"),
    (0, r"arrives from the south\.", "move south"),
    (0, r"You exit to the south\.", ""),
    (1, r"exits to the south\.", "move south"),
    (0, r"arrives from the north\.", "move east"),
    (0, r"You exit to the east\.", ""),
    (1, r"exits to the east\.", "move east"),
    (0, r"arrives from the west\.", "move west"),
    (0, r"You exit to the west\.", ""),
    (1, r"exits to the west\.", "move west"),
    (0, r"arrives from the east\.", "move up"),
    (0, r"You exit upward\.", ""),
    (1, r"exits upward\.", "move up"),
    (0, r"arrives from below\.", "move down"),
    (0, r"You exit downward\.", ""),
    (1, r"exits downward\.", "move down"),
    (0, r"arrives from above\.", ""),
)

test_actor_disappears = (
    (1, "> ", "quit"),
    (0, r"You suddenly wonder where .* went\.", ""),
)

test_account1_teardown = (
    (1, "What would you like to do?", "d"),
    (1, "Whom would you like to delete?", ""),
    (1, "What would you like to do?", "p"),
    (1, "permanently delete your account?", "y"),
    (1, "Disconnecting...", ""),
)

test_admin_setup = (
    (2, "Identify yourself:", "admin"),
    (2, "Enter your choice:", "n"),
    (2, 'Enter a new password for "admin":', "Test789"),
    (2, "Enter the same new password again:", "Test789"),
    (2, r"What would you like to do\?", "c"),
    (2, "Pick a birth gender for your new avatar:", "m"),
    (2, "Choose a name for him:", "1"),
    (2, "What would you like to do?", "a"),
    (2, "Whom would you like to awaken?", ""),
)

test_preferences = (
    (0, "> ", "preferences"),
    (0, r"\[32mprompt\x1b\[0m - <not set>.*> ", "preferences prompt $(foo)"),
    (0, r"\$\(foo\) ", "preferences prompt"),
    (0, r"\$\(foo\).*\$\(foo\) ", "preferences prompt $(time)>"),
    (0, "[0-9]> ", "preferences loglevel 0"),
    (0, "does not exist.*> ", "preferences prompt >"),
    (2, "> ", "preferences loglevel 0"),
    (2, "> ", "preferences"),
    (2, r"\[31mloglevel\x1b\[0m - 0.*> ", "preferences loglevel zero"),
    (2, r'''cannot be set to type "<class 'str'>"\..*> ''', ""),
)

test_crlf_eol = (
    # Send a CR+LF at the end of the line instead of the default CR+NUL,
    # to make sure they're treated the same
    (2, "> ", b"say I use CR+LF as my EOL, not CR+NUL.\r\n"),
    (2, r'You say, "I use CR\+LF as my EOL, not CR\+NUL\.".*> ', ""),
)

test_telnet_iac = (
    # Send a double (escaped) IAC byte within other text, which should get
    # unescaped and deduplicated to a single \xff in the buffer and then
    # the line of input discarded as a non-ASCII sequence
    (2, "> ", b"say argle\xff\xffbargle\r\0"),
    (2, r"Non-ASCII characters from admin: b'say.*argle\\xffbargle'.*> ", ""),
)

test_telnet_unknown_command = (
    # Send an unsupported negotiation command #127 which should get filtered
    # from the line of input
    (2, "> ", b"say glop\xff\x7fglyf\r\0"),
    (2, r'Ignored unknown command 127 from admin\..*"Glopglyf\.".*> ', ""),
)

test_telnet_unknown_option = (
    # Send an unassigned negotiation option #127 which should get logged
    (2, "> ", b"\xff\xfe\x7f\r\0"),
    (2, r'''Received "don't 127" from admin\..*> ''', ""),
)

test_admin_restriction = (
    (0, "> ", "help halt"),
    (0, r"That is not an available command\.", "halt"),
    (0, '(not sure what "halt" means|Arglebargle, glop-glyf)', ""),
)

test_admin_help = (
    (2, "> ", "help"),
    (2, r"halt.*Shut down the world\.", "help halt"),
    (2, "This will save all active accounts", ""),
)

test_help = (
    (0, "> ", "help say"),
    (0, r"See also: .*chat.*> ", ""),
)

test_abbrev = (
    (0, "> ", "h"),
    (0, r"h\[elp\].*m\[ove\].*> ", "he mo"),
    (0, r"Move in a specific direction\..*> ", "mov nor"),
    (0, r"You exit to the north\..*> ", "m s"),
    (0, r"You exit to the south\..*> ", ""),
)

test_reload = (
    (2, "> ", "reload"),
    (2, r"Reloading all code modules, configs and data\."
        r".* User admin reloaded the world\.",
     "show element account.admin"),
    (2, 'These are the properties of the "account.admin" element.*'
        r'  \x1b\[32mpasshash:\r\n\x1b\[31m\$.*> ', ""),
)

test_set_facet = (
    (2, "> ", "set actor.avatar_admin_0 gender female"),
    (2, r'You have successfully \(re\)set the "gender" facet of element', ""),
)

test_set_refused = (
    (2, "> ", "set mudpy.limit password_tries 10"),
    (2, r'The "mudpy\.limit" element is kept in read-only file', ""),
)

test_show_version = (
    (2, "> ", "show version"),
    (2, r"Running mudpy .* on .* Python 3.*with.*pyyaml.*> ", ""),
)

test_show_time = (
    (2, "> ", "show time"),
    (2, r"\r\n[0-9]+ increments elapsed.*> ", ""),
)

test_show_files = (
    (2, "> ", "show files"),
    (2, r'These are the current files containing the universe:.*'
        r'  \x1b\[31m\(rw\) \x1b\[32m/.*/account.yaml\x1b\[0m'
        r' \x1b\[33m\[private\]\x1b\[0m.*> ', ""),
)

test_show_file = (
    (2, "> ", "show file %s" %
        os.path.join(os.getcwd(), "data/internal.yaml")),
    (2, r'These are the nodes in the.*file:.*internal\.counters.*> ', ""),
)

test_show_groups = (
    (2, "> ", "show groups"),
    (2, r'These are the element groups:.*'
        r'  \x1b\[32maccount\x1b\[0m.*> ', ""),
)

test_show_group = (
    (2, "> ", "show group account"),
    (2, r'These are the elements in the "account" group:.*'
        r'  \x1b\[32maccount\.admin\x1b\[0m.*> ', ""),
)

test_show_element = (
    (2, "> ", "show element mudpy.limit"),
    (2, r'These are the properties of the "mudpy\.limit" element.*'
        r'  \x1b\[32mpassword_tries: \x1b\[31m3.*> ',
     "show element actor.avatar_admin_0"),
    (2, r'These are the properties of the "actor.avatar_admin_0" element.*'
        r'  \x1b\[32mgender: \x1b\[31mfemale.*> ', ""),
)

test_show_result = (
    (2, "> ", "show result 12345*67890"),
    (2, r"\r\n838102050\r\n.*> ", "show result 1/0"),
    (2, r"Your expression raised an exception.*division by zero.*> ", ""),
)

test_show_log = (
    (2, "> ", "show log"),
    (2, r"There are [0-9]+ log lines in memory and [0-9]+ at or above level "
        r"[0-9]+\. The matching lines\r\nfrom [0-9]+ to [0-9]+ are:", ""),
)

test_custom_loglevel = (
    (2, "> ", "set account.admin loglevel 2"),
    (2, "You have successfully .*> ", "show log"),
    (2, r"There are [0-9]+ log lines in memory and [0-9]+ at or above level "
        r"[0-9]+\. The matching lines\r\nfrom [0-9]+ to [0-9]+ are:", ""),
)

test_invalid_loglevel = (
    (2, "> ", "set account.admin loglevel two"),
    (2, r'''Value "two" of type "<class 'str'>" cannot be coerced .*> ''', ""),
)

test_log_no_errors = (
    (2, "> ", "show log 7"),
    (2, r"None of the [0-9]+ lines in memory matches your request\.", ""),
)

final_cleanup = (
    (0, "> ", "quit"),
    (0, "What would you like to do?", "d"),
    (0, "Whom would you like to delete?", ""),
    (0, "What would you like to do?", "p"),
    (0, "permanently delete your account?", "y"),
    (0, "Disconnecting...", ""),
    (2, "> ", "quit"),
    (2, "What would you like to do?", "d"),
    (2, "Whom would you like to delete?", ""),
    (2, "What would you like to do?", "p"),
    (2, "permanently delete your account?", "y"),
    (2, "Disconnecting...", ""),
)

dialogue = (
    (test_account0_setup, "first account setup"),
    (test_account1_setup, "second account setup"),
    (test_actor_appears, "actor spontaneous appearance"),
    (test_explicit_punctuation, "explicit punctuation"),
    (test_implicit_punctuation, "implicit punctuation"),
    (test_typo_replacement, "typo replacement"),
    (test_sentence_capitalization, "sentence capitalization"),
    (test_chat_mode, "chat mode"),
    (test_wrapping, "wrapping"),
    (test_forbid_ansi_input, "raw escape input is filtered"),
    (test_escape_macros, "replacement macros are escaped"),
    (test_movement, "movement"),
    (test_actor_disappears, "actor spontaneous disappearance"),
    (test_account1_teardown, "second account teardown"),
    (test_admin_setup, "admin account setup"),
    (test_preferences, "set and show preferences"),
    (test_crlf_eol, "send crlf from the client as eol"),
    (test_telnet_iac, "escape stray telnet iac bytes"),
    (test_telnet_unknown_command, "strip unknown telnet command"),
    (test_telnet_unknown_option, "log unknown telnet option"),
    (test_admin_restriction, "restricted admin commands"),
    (test_admin_help, "admin help"),
    (test_help, "help command"),
    (test_abbrev, "command abbreviation"),
    (test_reload, "reload"),
    (test_set_facet, "set facet"),
    (test_set_refused, "refuse altering read-only element"),
    (test_show_version, "show version and diagnostic info"),
    (test_show_time, "show elapsed world clock increments"),
    (test_show_files, "show a list of loaded files"),
    (test_show_file, "show nodes from a specific file"),
    (test_show_groups, "show groups"),
    (test_show_group, "show group"),
    (test_show_element, "show element"),
    (test_show_result, "show result of a python expression"),
    (test_show_log, "show log"),
    (test_custom_loglevel, "custom loglevel"),
    (test_invalid_loglevel, "invalid loglevel"),
    (test_log_no_errors, "no errors logged"),
    (final_cleanup, "delete remaining accounts"),
)


def start_service(config):
    # Clean up any previously run daemon which didn't terminate
    if os.path.exists(pidfile):
        pidfd = open(pidfile)
        pid = int(pidfd.read())
        try:
            # Stop the running service
            os.kill(pid, 15)
            time.sleep(1)
        except ProcessLookupError:
            # If there was no process, just remove the stale PID file
            os.remove(pidfile)
        # If there's a preexisting hung service, we can't proceed
        assert not os.path.exists(pidfile)

    # Clean up any previous test output
    for f in pathlib.Path(".").glob("capture_*.log"):
        # have to use .name here since remove() doesn't support passing a
        # PosixPath argument until Python3.6
        os.remove(f.name)
    for d in ("data", "var"):
        shutil.rmtree(d, ignore_errors=True)

    # Start the service and wait for it to be ready for connections
    service = subprocess.Popen(("mudpy", config),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    time.sleep(1)
    return(service)


def stop_service(service):
    success = True

    # The no-op case when no service was started
    if service is None:
        return(success)

    # This handles when the service is running as a direct child process
    service.terminate()
    returncode = service.wait(10)
    if returncode != 0:
        tlog("\nERROR: Service exited with code %s." % returncode)
        success = False

    # This cleans up a daemonized and disassociated service
    if os.path.exists(pidfile):
        pidfd = open(pidfile)
        pid = int(pidfd.read())
        try:
            # Stop the running service
            os.kill(pid, 15)
            time.sleep(1)
        except ProcessLookupError:
            # If there was no process, just remove the stale PID file
            os.remove(pidfile)
        # The PID file didn't disappear, so we have a hung service
        if os.path.exists(pidfile):
            tlog("\nERROR: Hung daemon with PID %s." % pid)
            success = False

    # Log the contents of stdout and stderr, if any
    stdout, stderr = service.communicate()
    tlog("\nRecording stdout as capture_stdout.log.")
    serviceout = open("capture_stdout.log", "w")
    serviceout.write(stdout.decode("utf-8"))
    tlog("\nRecording stderr as capture_stderr.log.")
    serviceerr = open("capture_stderr.log", "w")
    serviceerr.write(stderr.decode("utf-8"))

    return(success)


def tlog(message, quiet=False):
    logfile = "capture_tests.log"
    with open(logfile, "a") as logfd:
        logfd.write(message + "\n")
    if not quiet:
        sys.stdout.write(message)
    return True


def option_callback(telnet_socket, command, option):
    if option == b'\x7f':
        # We use this unassigned option value as a canary, so short-circuit
        # any response to avoid endlessly looping
        pass
    elif command in (telnetlib.DO, telnetlib.DONT):
        telnet_socket.send(telnetlib.IAC + telnetlib.WONT + option)
    elif command in (telnetlib.WILL, telnetlib.WONT):
        telnet_socket.send(telnetlib.IAC + telnetlib.DONT + option)


def main():
    captures = ["", "", ""]
    lusers = [telnetlib.Telnet(), telnetlib.Telnet(), telnetlib.Telnet()]
    success = True
    start = time.time()
    service = None
    if len(sys.argv) > 1:
        # Start the service if a config file was provided on the command line
        service = start_service(sys.argv[1])
    for luser in lusers:
        luser.open("::1", 4000)
        luser.set_option_negotiation_callback(option_callback)
    for test, description in dialogue:
        tlog("\nTesting %s..." % description)
        test_start = time.time()
        for conversant, question, answer in test:
            tlog("luser%s waiting for: %s" % (conversant, question),
                 quiet=True)
            try:
                index, match, received = lusers[conversant].expect(
                    [re.compile(question.encode("utf-8"), flags=re.DOTALL)], 5)
                captures[conversant] += received.decode("utf-8")
            except ConnectionResetError:
                tlog("\nERROR: Unable to connect to server.")
                success = False
                break
            except EOFError:
                tlog("\nERROR: luser%s premature disconnection expecting:\n\n"
                     "%s\n\n"
                     "Check the end of capture_%s.log for received data."
                     % (conversant, question, conversant))
                success = False
                break
            try:
                captures[conversant] += lusers[
                    conversant].read_very_eager().decode("utf-8")
            except Exception:
                pass
            if index != 0:
                tlog("\nERROR: luser%s did not receive expected string:\n\n"
                     "%s\n\n"
                     "Check the end of capture_%s.log for received data."
                     % (conversant, question, conversant))
                success = False
                break
            if type(answer) is str:
                tlog("luser%s sending: %s" % (conversant, answer), quiet=True)
                lusers[conversant].write(("%s\r\0" % answer).encode("utf-8"))
                captures[conversant] += "%s\r\n" % answer
            elif type(answer) is bytes:
                tlog("luser%s sending raw bytes: %s" % (conversant, answer),
                     quiet=True)
                lusers[conversant].get_socket().send(answer)
                captures[conversant] += "!!!RAW BYTES: %s" % answer
            else:
                tlog("\nERROR: answer provided with unsupported type %s"
                     % type(answer))
                success = False
                break
        if not success:
            break
        tlog("Completed in %.3f seconds." % (time.time() - test_start))
    duration = time.time() - start
    for conversant in range(len(captures)):
        try:
            captures[conversant] += lusers[
                conversant].read_very_eager().decode("utf-8")
        except Exception:
            pass
        lusers[conversant].close()
        logfile = "capture_%s.log" % conversant
        tlog("\nRecording session %s as %s." % (conversant, logfile))
        log = open(logfile, "w")
        log.write(captures[conversant])
        log.close()
    if not stop_service(service):
        success = False
    tlog("\nRan %s tests in %.3f seconds." % (len(dialogue), duration))
    if success:
        tlog("\nSUCCESS\n")
    else:
        tlog("\nFAILURE\n")
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
