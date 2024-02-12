#!/usr/bin/python3

import requests as req
import argparse
import re

parser = argparse.ArgumentParser(description='Enumerates valid email addresses from Office 365 without submitting login attempts.')
parser.add_argument('-e', '--email', help='Single email address to validate.')
parser.add_argument('-f', '--file', help='List of email addresses to validate, one per line.')
parser.add_argument('-o', '--output', help='Output valid email addresses to the specified file.')
args = parser.parse_args()

url = 'https://login.microsoftonline.com/common/GetCredentialType'

def main():
    if args.file is not None:
        with open(args.file) as file:
            for line in file:
                with req.session() as s:
                    email = line.strip()  # Removes whitespace
                    body = '{"Username":"%s"}' % email
                    headers = {'Content-Type': 'application/json'}  # Specify content type
                    request = s.post(url, data=body, headers=headers)
                    response = request.text
                    valid = re.search('"IfExistsResult":0,', response)
                    invalid = re.search('"IfExistsResult":1,', response)
                    if invalid:
                        print(f'{email} - INVALID')
                    if valid:
                        print(f'{email} - VALID')
                        if args.output is not None:
                            with open(args.output, 'a+') as output_file:
                                output_file.write(email + '\n')

    elif args.email is not None:
        email = args.email
        body = '{"Username":"%s"}' % email
        headers = {'Content-Type': 'application/json'}  # Specify content type
        request = req.post(url, data=body, headers=headers)
        response = request.text
        valid = re.search('"IfExistsResult":0', response)
        invalid = re.search('"IfExistsResult":1', response)
        if invalid:
            print(f'{email} - INVALID')
        if valid:
            print(f'{email} - VALID')
            if args.output is not None:
                with open(args.output, 'w') as output_file:
                    output_file.write(email + '\n')

if __name__ == "__main__":
    main()
