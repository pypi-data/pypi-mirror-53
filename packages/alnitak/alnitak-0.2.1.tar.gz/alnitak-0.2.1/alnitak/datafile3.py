
import os
import json
from alnitak import prog as Prog
from alnitak import dane


# TODO: datafile should have a checksum on its data.

def read(prog):
    prog.log.info1("+++ reading datafile '{}'".format(prog.datafile))

    try:
        with open(str(prog.datafile), "r") as file:
            prog.data = json.load(file)
    except ValueError as ex:
        # JSON error: exception thrown is json.JSONDecodeError in python 3.5+.
        # For python 3.4, it is ValueError.
        prog.log.error(
                "datafile '{}': {}".format(prog.datafile, str(ex).lower()))
        return Prog.RetVal.exit_failure
    except FileNotFoundError as ex:
        prog.log.info1("  + no file to read")
        return Prog.RetVal.exit_ok
    except OSError as ex:
        prog.log.error(
                "datafile '{}': {}".format(ex.filename, ex.strerror.lower()))
        return Prog.RetVal.exit_failure

    return Prog.RetVal.ok


def read_prehook(prog):
    # config file read and prog.target_list is set. If some targets have
    # already been processed, then they will have
    #
    #
    # datafile: example.com, with old config params
    # config: example.com, with new config params
    # Q: what happens?
    # A: if datafile entry is prehook, then amend it with the new config
    #    file data; if it is posthook, then ignore the new config params.
    #
    ret = read(prog)
    if ret == Prog.RetVal.exit_failure:
        return ret

    # no datafile
    if ret == Prog.RetVal.exit_ok:
        dane.set_data(prog)
        return Prog.RetVal.ok

    # datafile exists
    for t in prog.target_list:
        for domain in prog.data['data']:
            if t.domain == domain:
                # if posthook has already run, then we will not make any
                # changes (if present) from the config file. We will just
                # leave the data as it is.
                if prog.data['data'][domain]['status'] != 'prepare':
                    break
                # if only prehook has been run, then we will update the
                # data.
                else:
                    new = t.data(prog)
                    old = prog.data['data'][domain]
                    # if dane_dir AND le_dir are the same, then keep the
                    # 'certs' values the same.
                    if (new['config']['dane_directory']
                                    == old['config']['dane_directory']
                            and new['config']['letsencrypt_directory']
                                    == old['config']['letsencrypt_directory']):
                        prog.data['data'][domain] = new
                        prog.data['data'][domain]['certs'] = old['certs']
                    else:
                        prog.data['data'][domain] = new
                    break
    return ret



def write(prog):
    prog.log.info1("+++ writing to datafile '{}'".format(prog.datafile))

    if not prog.data['data']:
        prog.log.info1("  + no data to write")
        return remove(prog)

    with open('./d3.data', 'w') as file:
        json.dump(prog.data, file, indent=2)

    return Prog.RetVal.ok



def write_prehook(prog):
    """Write to datafile based on prehook mode operation ('prehook lines').

    In prehook mode, the datafile needs to write lines (called
    'prehook lines') that tell subsequent calls of the program what
    certificate live/archive files are, and where. This function will also
    set the permissions of the datafile properly: permissions are changed
    before any meaningful data is written.

    Args:
        prog (State): contains the data to write.

    Returns:
        RetVal: returns 'RetVal.exit_failure' if any errors encountered,
            'RetVal.ok' for success.
    """
    prog.log.info1(
            "+++ writing datafile (prehook): '{}'".format(prog.datafile))

    try:
        prog.datafile.parent.mkdir(parents=True)
    except FileExistsError as ex:
        # Note: this catch can be removed for python 3.5+ since mkdir()
        # accepts the 'exist_ok' parameter.
        if prog.datafile.parent.is_dir():
            # if directory exists, that is fine
            pass
        else:
            prog.log.error(
                "creating datafile directory '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
            return Prog.RetVal.exit_failure
    except OSError as ex:
        prog.log.error(
            "creating datafile directory '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return Prog.RetVal.exit_failure

    if not prog.data['data']:
        prog.log.info1("  + no data to write")
        return remove(prog)
        # FIXME: no datafile on prehook! Should probably emit a warning
        # message? But only if there are errors that have caused this and
        # not because no domains in config file?

    # datafile must be root:root, 0600
    with open(str(prog.datafile), "w") as file: # FIXME XXX
        json.dump(prog.data, file, indent=2)    # FIXME XXX
    return Prog.RetVal.ok                       # FIXME XXX
    # NOTE: follow: <https://stackoverflow.com/questions/5624359/write-file-with-specific-permissions-in-python/15015748>
    #

    try:
        with open(str(prog.datafile), "a") as file:
            file.write('{}')
    except OSError as ex:
        prog.log.error("writing datafile '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return Prog.RetVal.exit_failure

    if fix_permissions(prog):
        return Prog.RetVal.exit_failure

    try:
        with open(str(prog.datafile), "a") as file:
            json.dump(prog.data, file, indent=2)
    except OSError as ex:
        prog.log.error("writing datafile '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return Prog.RetVal.exit_failure

    return Prog.RetVal.ok

def write_posthook(prog):
    """Write to datafile based on posthook mode operation ('posthook lines').

    In posthook mode, the datafile needs to write lines (called
    'posthook lines') that record what DANE records were published, or need
    to be published or deleted, in addition to appropriate prehook lines,
    which will have been previously read into the internal program state
    object. This function will also set the permissions of the datafile
    properly: permissions are changed before any meaningful data is written.

    Args:
        prog (State): contains the data to write.

    Returns:
        RetVal: returns 'RetVal.exit_failure' if any errors encountered,
            'RetVal.ok' for success.
    """
    prog.log.info1("+++ writing to datafile '{}'".format(prog.datafile))

    if not prog.data['data']:
        prog.log.info1("  + no data to write")
        return remove(prog)

    # datafile must be root:root, 0600
    with open(str(prog.datafile), "w") as file: # FIXME XXX
        json.dump(prog.data, file, indent=2)    # FIXME XXX
    return Prog.RetVal.ok                       # FIXME XXX
    # NOTE: follow: <https://stackoverflow.com/questions/5624359/write-file-with-specific-permissions-in-python/15015748>
    #

    try:
        with open(str(prog.datafile), "w") as file:
            file.write('{}')
    except OSError as ex:
        prog.log.error("writing datafile '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return Prog.RetVal.exit_failure

    if fix_permissions(prog):
        return Prog.RetVal.exit_failure

    try:
        with open(str(prog.datafile), "a") as file:
            json.dump(prog.data, file, indent=2)
    except OSError as ex:
        prog.log.error("writing datafile '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return Prog.RetVal.exit_failure

    return Prog.RetVal.ok

def remove(prog):
    """Remove the datafile, if it exists.

    If the datafile does not exist, we won't look a gift horse in the
    mouth...

    Args:
        prog (State): not modified.

    Returns:
        RetVal: returns 'RetVal.exit_failure' if any errors encountered,
            'RetVal.ok' for success. 
    """
    prog.log.info1("+++ removing datafile '{}'".format(prog.datafile))

    # if in reset mode, we do not want to remove the datafile if it exists,
    # unless the '--force' flag has been given.
    if prog.recreate_dane:
        if prog.datafile.exists():
            if not prog.force:
                prog.log.error("datafile exists; will not continue (use '--force' to override)")
                return Prog.RetVal.exit_failure
        else:
            prog.log.info1("  + datafile not found; ok")
            return Prog.RetVal.ok

    try:
        prog.datafile.unlink()
    except FileNotFoundError as ex:
        return Prog.RetVal.ok
    except OSError as ex:
        prog.log.error("removing datafile '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return Prog.RetVal.exit_failure

    prog.log.info1("  + datafile removed")
    return Prog.RetVal.ok

def fix_permissions(prog):
    """Ensure the datafile has the correct permissions.

    'Correct' means mode 0600 and owned by root:root.

    Args:
        prog (State): not modified (except for logging).

    Returns:
        RetVal: returns 'True' if any errors encountered, 'False' for
            success. 
    """
    prog.log.info3(" ++ checking/fixing mode of datafile: should be '0600'")
    try:
        prog.datafile.chmod(0o600)
    except OSError as ex:
        prog.log.error(
            "changing permissions of datafile '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return True

    prog.log.info3(
            " ++ checking/fixing owner of datafile: should be 'root:root'")
    try:
        if not prog.testing_mode:
            os.chown(str(prog.datafile), 0, 0)
    except OSError as ex:
        prog.log.error(
                "changing owner of datafile '{}' failed: {}".format(
                                            ex.filename, ex.strerror.lower()))
        return True

    return False

