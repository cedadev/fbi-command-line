# FBI Command Line Utility
This package provides a command line utility to explore the Elasticsearch
file system.

## Running the utility

1. Run a single known command
    ```bash
    fbi_cmdline <command> <args>
    ```
2. Explore commands or run multiple
    ```bash
    fbi_cmdline
    ```
    
    This will drop you into the interactive environment:
    ```bash
    $ fbi_cmdline
    FBI cmd>
    ```
    
    From here you can type help to see all available commands and get 
    descriptions about them
    
## Adding new commands

This package is designed to be easily extendable.
To create a new command:
1. Make a new file in the `fbi_cmdline/commands` directory with the same
name as your command.
2. Set your file up with the following structure. 
    ```python
   from .registery import CommandRegistry
    
    
   @CommandRegistry.register
   class CommandName(object):
      command_name = 'commandname' #This is what will be called at the command line
       
      @classmethod
      def dir_query(cls, path):
         return {}
        
      @classmethod
      def fbi_query(cls, path):
          return {}
        
      @classmethod
      def help(cls, cmdcls):
        """
          This will be run when help <command_name> is called.
          This method should print help information.
          :param cmdcls: The command line class running the command (likely un-used)
         """
        pass
        
      @classmethod
      def run_command(cls, cmdcls, line):
         """
          This will be run when the command is called
          :param cmdcls: The command line class running the command
          :param line: String of the arguments supplied to the command
         """
         pass
    
    ```
    Methods should be class methods to be available without first creating a
    class instance
    
3. Register your new command with the command line utility.
You should already have your class decorated with the register function. 
To complete the registration, import your command in the commands init.py
`fbi_cmdline/commands/__init__.py` eg.:
    ```python
    # Import command classes
    from  .dataset_count import DatasetCount
    
    ```

    Your command should now be available through the command line utility