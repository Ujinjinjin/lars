class PargValidator:
    @staticmethod
    def single_value(*args) -> bool:
        value_count: int = 0
        for arg in args:
            if arg is not None:
                value_count += 1

        return value_count == 1

    @staticmethod
    def all_values(*args) -> bool:
        value_count: int = 0
        for arg in args:
            if arg is not None:
                value_count += 1

        return value_count == len(args)
