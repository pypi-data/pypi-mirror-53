from __future__ import print_function

import json
import os.path
import re
import sys
try:
    from dotty_dict import dotty
except:
    dotty = None

if sys.version_info[0] < 3:
    from io import open

class KeywordExpander:
    """
    Parse input file or stream line by line, performing keyword expansion from saved json state.

    ...

    Methods
    -------
    expand_from_json(data, output_directory):
        Given current json, read code_src and write code_snap
    expand_from_json_file(infile, output_directory):
        Given json input file, read code_src and write code_snap
    """

    # Note in this first case that {} are explicitly omitted and there is no <end_fmt>
    _var_expand_str = r'(?P<pre>.*)[$](?P<inline>[!]?)(?P<var>[a-zA-Z_][a-zA-Z_0-9.]*)(?P<col>:?:?)(?P<curval>.*)[$](?P<post>.*)'
    _var_expand_br_str = r'(?P<pre>.*)[$](?P<inline>[!]?)[{](?P<var>[a-zA-Z_][a-zA-Z_0-9.]*)(?P<end_fmt>:?[^:]*[}])(?P<col>:?:?)(?P<curval>.*)[$](?P<post>.*)'

    _var_expand_re = re.compile(_var_expand_str, re.S)
    _var_expand_br_re = re.compile(_var_expand_br_str, re.S)

    @staticmethod
    def _lookup_var(s, data):
        from psnap import state_tracker
        meta_key = state_tracker.StateTracker._meta_key

        data_key = data[meta_key]["data_key"]

        # data uses dotty_dict so can use any dotted notation directly
        if s in data[data_key]:
            return data[data_key][s]

        return None

    @staticmethod
    def _expand_vars(line, data):
        # Try to return quickly if see nothing to expand
        if not "$" in line:
            return line

        # Search is for match anywhere on line
        # but we are matching to full line.
        #match = KeywordExpander._var_expand_re.search(line)
        # Try to match braces first but fallback if not found
        match = KeywordExpander._var_expand_br_re.match(line)
        if match is None:
            match = KeywordExpander._var_expand_re.match(line)

        if match is not None:
            d = match.groupdict()
            val = KeywordExpander._lookup_var(d['var'], data)
            fmt = ""
            ob = ""
            end_fmt = ""
            if 'end_fmt' in d and d['end_fmt'] is not None:
                ob = "{"
                end_fmt = d['end_fmt']
                fmt = "{" + end_fmt
            if val is not None:
                val_formatted = val
                if len(fmt) > 0:
                    val_formatted = fmt.format(val)
                coltype = d['col']
                if len(coltype) == 0:
                    coltype = ":"
                # Note that curval contains the whitespace but is unused
                if d['inline'] == "!":
                    # Replace from $...$ with just {val_formatted}
                    line = "{}{}{}".format(d['pre'], val_formatted, d['post'])
                else:
                    # Maintain line but rewrite value
                    line = "{}${}{}{}{} {} ${}".format(d['pre'], ob, d['var'], end_fmt, coltype, val_formatted, d['post'])

        return line

    @staticmethod
    def expand_from_json(data, output_directory=None):
        """
        Given current json, read code_src and write code_snap.

        Parameters
        ----------
        data : dict
            json dictionary include psnap metadata and state data.
        output_directory : str, optional
            Output directory for code_snap else default is to use same directory as code_src.

        Raises
        ------
        RuntimeError
            Issues RuntimeError if output of code_snap matches input code_src.

        Returns
        -------
        dict
            Dictionary containing "code_src" and "code_snap".
        """
        from psnap import state_tracker
        meta_key = state_tracker.StateTracker._meta_key

        infile = data[meta_key]['code_src']
        outfile = data[meta_key]['code_snap']

        if output_directory is not None:
            # Update path in outfile to use output_directory
            output_basename = os.path.basename(outfile)
            outfile = os.path.join(output_directory, output_basename)

        infile_norm = os.path.normpath(infile)
        outfile_norm = os.path.normpath(outfile)
        if infile_norm == outfile_norm:
            raise RuntimeError("Output file must not match input code_src: {}".format(infile))

        # See if output_directory exists or needs to be created
        output_directory = os.path.dirname(outfile)
        if len(output_directory) > 0 and not os.path.exists(output_directory):
            os.makedirs(output_directory)

        with open(outfile, "w", encoding="utf-8") as fout:
            with open(infile, encoding="utf-8") as fin:
                for line in fin:
                    line = KeywordExpander._expand_vars(line, data)
                    if sys.version_info[0] > 2:
                        fout.write(line)
                    else:
                        fout.write(line.decode('utf-8'))

        result = {
            "code_src": infile,
            "code_snap": outfile
        }

        return result

    @staticmethod
    def expand_from_json_file(infile, output_directory=None):
        """
        Given json input file, read code_src and write code_snap.

        Parameters
        ----------
        infile : str
            filename of json dictionary include psnap metadata and state data.
        output_directory : str, optional
            Output directory for code_snap else default is to use same directory as code_src.

        Returns
        -------
        dict
            Dictionary containing "code_src" and "code_snap".
        """
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)
            if dotty is not None:
                from psnap import state_tracker
                meta_key = state_tracker.StateTracker._meta_key
                data_key = data[meta_key]["data_key"]
                data[data_key] = dotty(data[data_key])

        return KeywordExpander.expand_from_json(data, output_directory=output_directory)
