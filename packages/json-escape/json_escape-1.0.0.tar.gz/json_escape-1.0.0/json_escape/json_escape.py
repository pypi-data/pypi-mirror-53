import json
import click
import sys 

def json_escape(json_string):
    json_deserialized = json.dumps(json.loads(json_string))
    return json.dumps(json_deserialized)


def json_unescape(json_string):
    unescaped_json_string = bytes(json_string, 'utf-8').decode('unicode_escape').strip('"')
    json_deserialized = json.loads(unescaped_json_string)
    return json.dumps(json_deserialized, indent=4, ensure_ascii=False)


def read_from_file(path_to_file):
    with open(path_to_file) as json_f:
        return json_f.read()


def write_to_file(json_content, output_path):
    with open(output_path, 'w') as output_f:
        output_f.write(json_content)


@click.command()
@click.argument('input_file')
@click.option('--operation', default='escape', help='escape/unescape json string')
@click.option('--output', default=None, help='Path to the output file')
def process_json(input_file, operation, output):
    file_content = read_from_file(input_file)    
    operations = {
        'escape': json_escape,
        'unescape': json_unescape,
    }
    if operation not in operations:
        click.echo('Unknown operation {}'.format(operation))
        sys.exit(1)
    operation = operations[operation]
    processed_json = operation(file_content)
    if output is None:
        click.echo(processed_json)
    else:
        write_to_file(processed_json, output)


def main():
    process_json()


if __name__ == "__main__":
    main()
