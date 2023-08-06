"""


cli for convert


"""


from . import utils


class CLICommand:
    """Convert between file formats.

    Use "-" for stdin/stdout.
    See "chemio info --formats" for known formats.
    """

    @staticmethod
    def add_arguments(parser):
        add = parser.add_argument
        add('-v', '--verbose', action='store_true',
            help='Print names of converted files')
        add('input',  # nargs='+',
            metavar='input-file')
        add('-i', '--input-format', metavar='FORMAT',
            help='Specify input FORMAT')
        add('output', metavar='output-file')
        add('-o', '--output-format', metavar='FORMAT',
            help='Specify output FORMAT')
        add('-f', '--force', action='store_true',
            help='Overwrite an existing file')
        add('-n', '--image-number',
            default=':', metavar='NUMBER',
            help='Pick images from trajectory.  NUMBER can be a '
            'single number (use a negative number to count from '
            'the back) or a range: start:stop:step, where the '
            '":step" part can be left out - default values are '
            '0:nimages:1.')
        add('--data', nargs='*',
            help='data to be posted, key=val format')
        add('--calc_data', nargs='*',
            help='calc data to be posted, key=val format')
        # add('-e', '--exec-code',
        #     help='Python code to execute on each atoms before '
        #     'writing it to output file. The Atoms object is '
        #     'available as `atoms`. Set `atoms.info["_output"] = False` '
        #     'to suppress output of this frame.')
        # add('-E', '--exec-file',
        #     help='Python source code file to execute on each '
        #     'frame, usage is as for -e/--exec-code.')
        # add('-a', '--arrays',
        #     help='Comma-separated list of atoms.arrays entries to include '
        #     'in output file. Default is all entries.')
        # add('-I', '--info',
        #     help='Comma-separated list of atoms.info entries to include '
        #     'in output file. Default is all entries.')
        add('-s', '--split-output', action='store_true',
            help='Write output frames to individual files. '
            'Output file name should be a format string with '
            'a single integer field, e.g. out-{:0>5}.xyz')

    @staticmethod
    def run(args, parser):
        if args.verbose:
            print(', '.join(args.input), '->', args.output)
        # if args.arrays:
        #     args.arrays = [k.strip() for k in args.arrays.split(',')]
        #     if args.verbose:
        #         print('Filtering to include arrays: ', ', '.join(args.arrays))
        # if args.info:
        #     args.info = [k.strip() for k in args.info.split(',')]
        #     if args.verbose:
        #         print('Filtering to include info: ', ', '.join(args.info))

        configs = []
        # for filename in args.input:
        #     atoms = read(filename, args.image_number, format=args.input_format)
        #     # print(atoms)
        #     if isinstance(atoms, list):
        #         configs.extend(atoms)
        #     else:
        #         configs.append(atoms)

        # if args.debug:
        #     print(configs)
        # # new_configs = []
        # # for atoms in configs:
        # #     if args.arrays:
        # #         atoms.arrays = dict((k, atoms.arrays[k]) for k in args.arrays)
        # #     if args.info:
        # #         atoms.info = dict((k, atoms.info[k]) for k in args.info)
        # #     if args.exec_code:
        # #         # avoid exec() for Py 2+3 compat.
        # #         eval(compile(args.exec_code, '<string>', 'exec'))
        # #     if args.exec_file:
        # #         eval(compile(open(args.exec_file).read(), args.exec_file, 'exec'))
        # #     if  "_output" not in atoms.info or atoms.info["_output"]:
        # #         new_configs.append(atoms)
        # # configs = new_configs

        # if not args.force and os.path.isfile(args.output):
        #     parser.error('File already exists: {}'.format(args.output))

        # if len(configs) == 1:
        #     if args.debug:
        #         print('only 1 image')
        #     write(args.output, configs[0], format=args.output_format)
        # elif args.split_output:
        #     if args.debug:
        #         print('{0} images and split'.format(len(configs)))
        #     for i, atoms in enumerate(configs):
        #         write(args.output.format(i), atoms, format=args.output_format)
        # else:
        #     if args.debug:
        #         print('{0} images and not split'.format(len(configs)))
        #     write(args.output, configs, format=args.output_format)
        data = utils.parse_args_data(args.data)
        calc_data = utils.parse_args_data(args.calc_data)
        import chemio, logging
        if args.debug:
            chemio.main.logger.setLevel(logging.DEBUG)
        chemio.convert(args.input, args.output, args.image_number,
                args.input_format, args.output_format,
                format_nocheck=args.nocheck,
                data=data, calc_data=calc_data)
