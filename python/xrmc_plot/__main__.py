#!/usr/bin/env python3

import argparse
import xrmc
import sys

def main():
    parser = argparse.ArgumentParser(description='Plots XRMC output-files')
    parser.add_argument('--ScatOrderNum', type=int, help='Plot only contribution for N interactions', metavar='N')
    parser.add_argument('--write-to-csv', type=str, help='Write plot to CSV file FILENAME', metavar='FILENAME')
    parser.add_argument('output-file', type=str)
    args = parser.parse_args()
    #print(args)
    #print(vars(args)['ScatOrderNum'])
    #print(vars(args)['write_to_csv'])
    #print(vars(args)['output-file'])

    try:
        data = xrmc.Output(vars(args)['output-file'])
        if (vars(args)['write_to_csv']):
            data.write_to_csv(vars(args)['write_to_csv'], ScatOrderNum=vars(args)['ScatOrderNum'])
        data.plot(ScatOrderNum=vars(args)['ScatOrderNum'])
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
