#!/usr/bin/python3
""" entry point of the command interpreter """
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import sys
from shlex import split
import models


class HBNBCommand(cmd.Cmd):
    """class HBNBCommand """

    prompt = "(hbnb) "
    clsz = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place', 'Review']

    def __init__(self, *args, **kwargs):
        '''Initialization'''
        super().__init__(*args, **kwargs)
        self.file_storage = FileStorage()

    # handling quit
    def do_quit(self, args):
        """Quit command to exit the program

        """
        sys.exit()

    # handling EOF
    def do_EOF(self, args):
        """Exit the program on EOF (Ctrl+D)"""
        print()
        sys.exit()

    def do_help(self, args):
        """help"""
        cmd.Cmd.do_help(self, args)

    # an empty line + ENTER shouldn’t execute anything
    def emptyline(self):
        """Handles an empty line; do nothing."""
        pass

    # task 7 starts here
    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        try:
            if not line:
                raise SyntaxError()

            class_name, *params = line.split()
            if class_name not in self.clsz:
                print("** class doesn't exist **")
                return

            kwargs = {}
            for param in params:
                key, value = param.split("=")
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1].replace('\\"', '"').replace('_', ' ')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        print(f"Invalid float value: {value}")
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        print(f"Invalid integer value: {value}")
                        continue
                kwargs[key] = value

            obj = eval(class_name)(**kwargs)
            storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_show(self, args):
        """Prints str representation of instance based on class name and id"""
        if not args:
            print('** class name missing **')
        elif args.split()[0] not in HBNBCommand.clsz:
            print("** class doesn't exist **")
        if len(args.split()) < 2:
            print('** instance id missing **')
        else:
            class_name, instance_id = args.split()[0], args.split()[1]
            key = "{}.{}".format(class_name, instance_id)
            instances = storage.all()

            if key not in instances:
                print('** no instance found **')
            else:
                print(instances[key])

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        if not args:
            print('** class name missing **')
        elif args.split()[0] not in HBNBCommand.clsz:
            print("** class doesn't exist **")
        elif len(args.split()) < 2:
            print('** instance id missing **')
        else:
            class_name, instance_id = args.split()[0], args.split()[1]
            key = "{}.{}".format(args.split()[0], args.split()[1])
            instances = storage.all()

            if key not in instances:
                print('** no instance found **')
            else:
                del instances[key]
                storage.save()

    def do_all(self, args):
        """Prints all string representation of all instances"""
        storage.reload()
        instances = storage.all()

        if not args or args.lower() == 'basemodel':
            result = [instance.__str__() for instance in instances.values()]
            print(result)

        elif args.split()[0] in HBNBCommand.clsz:
            result = [
                instance.__str__()
                for key, instance in instances.items()
                if key.split('.')[0] == args.lower()
            ]
            print(result)
        else:
            print("** class doesn't exist **")

            # task 7 ends here
    """
    def do_update(self, args):
        #'''Update Console instance'''
        if not args:
            print('** class name missing **')
        else:
            if split(args)[0] not in self.clsz:
                print("** class doesn't exist **")
            elif len(split(args)) < 2:
                print('** instance id missing **')
            else:
                key = "{}.{}".format(split(args)[0], split(args)[1])
                instances = storage.all()
                if key not in instances:
                    print('** no instance found **')
                elif len(split(args)) < 3:
                    print('** attribute name missing **')
                elif len(split(args)) < 4:
                    print('** value missing **')
                else:
                    setattr(instances[key], split(args)[2], split(args)[3])
                    instances[key].save()
    """

    def do_update(self, args):
        '''Update Console instance'''
        if not args:
            print('** class name missing **')
        else:
            split_args = split(args)
            if split_args[0] not in self.clsz:
                print("** class doesn't exist **")
            elif len(split_args) < 2:
                print('** instance id missing **')
            else:
                key = "{}.{}".format(split_args[0], split_args[1])
                instances = storage.all()
                if key not in instances:
                    print('** no instance found **')
                elif len(split_args) < 3:
                    print('** attribute name missing **')
                elif len(split_args) < 4:
                    print('** value missing **')
                else:
                    setattr(instances[key], split_args[2], split_args[3])
                    try:
                        instances[key].save()
                    except Exception as e:
                        print(f"Error updating instance: {str(e)}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
