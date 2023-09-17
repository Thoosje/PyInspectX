class Utils:
    @staticmethod
    def pretty_print_dict(data, indent=0):
        """
        Formats a dictonary in a readable string that can be printend.

        Args:
            dict: Dict that has to be formatted.
            indent (int, optional): The indention that will be used to print. Default is 0.

        Returns:
            str: Formatted string.
        """

        pretty_result = ""
        for key, value in data.items():
            if isinstance(value, dict):
                pretty_result += " " * indent + f"{key}:\n"
                pretty_result += Utils.pretty_print_dict(value, indent + 4)
            else:
                pretty_result += " " * indent + f"{key}: {value}\n"

        return pretty_result
