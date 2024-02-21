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

    def do_create(self, args):
        """ Create an object of any class"""
        try:
            if not args:
                raise SyntaxError()
            split1 = args.split(' ')
            new_instance = eval('{}()'.format(split1[0]))
            params = split1[1:]
            for param in params:
                k, v = param.split('=')
                try:
                    attribute = HBNBCommand.verify_attribute(v)
                except:
                    continue
                if not attribute:
                    continue
                setattr(new_instance, k, attribute)
            new_instance.save()
            print(new_instance.id)
        except SyntaxError:
            print("** class name missing **")
        except NameError as e:
            print("** class doesn't exist **")

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
        """ Shows all objects, or all objects of a class"""
        print_list = []

        __objects = storage.all()
        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.clsz:
                print("** class doesn't exist **")
                return
            for k, v in __objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in __objects.items():
                print_list.append(str(v))

        print(print_list)

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

    @classmethod
    def verify_attribute(cls, attribute):
        """
        Verify if the attribute is correctly formatted
        """
        if attribute[0] is attribute[-1] in ['"', "'"]:
            return attribute.strip('"\'').replace('_', ' ').replace('\\', '"')
        else:
            try:
                try:
                    return int(attribute)
                except ValueError:
                    return float(attribute)
            except ValueError:
                return None


if __name__ == '__main__':
    HBNBCommand().cmdloop()
