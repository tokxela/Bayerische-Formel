import configparser


class Config:

    def __init__(self):
        self.path = "settings.ini"
        self.file = configparser.ConfigParser()
        self.file.add_section("Settings")
        self.config = None

    def new_config(self):
        try:
            pmax = int(input("Maximal grade in your grades system: "))
            pmin = int(input("Minimal positive grade in your grades system: "))
        except TypeError:
            print("An error occurred, try again")
            self.new_config()
        self.file.set("Settings", "pmax", str(pmax))
        self.file.set("Settings", "pmin", str(pmin))
        with open(self.path, "w") as config_file:
            self.file.write(config_file)

    def get_info(self):
        self.file.read(self.path)
        return [self.file["Settings"]["pmax"], self.file["Settings"]["pmin"]]


class Console:

    def __init__(self):
        self.config = Config()
        self.main()

    def main(self):
        options = ["Config edit", "From your to german grades", "From german to your grades", "Additional information"]
        print("Select an option:")
        for i in range(len(options)):
            print(f"{i+1} - {options[i]}")
        try:
            selected_option = int(input('Select option: '))
        except ValueError:
            print("Input error. Try again")
            self.main()
        if selected_option > len(options):
            print("Option nummer error. Try again")
            self.main()
        elif selected_option == 1:
            self.config.new_config()
            self.main()
        elif selected_option == 2:
            self.from_your()
        elif selected_option == 3:
            self.to_your()
        elif selected_option == 4:
            self.additional_information()

    def from_your(self):
        formula = Formula(self.config)
        try:
            n = float(input("Your grade: "))
        except ValueError:
            print("An error occurred, try again")
            self.from_your()
        print(f"Your mark {n} = {formula.calculate_to(n)}")
        self.main()

    def additional_information(self):
        print("https://de.wikipedia.org/wiki/Bayerische_Formel")
        self.main()

    def to_your(self):
        formula = Formula(self.config)
        try:
            n = float(input("Your grade: "))
        except ValueError:
            print("An error occurred, try again")
            self.from_your()
        print(f"Your mark {n} = {formula.calculate_from(n)}")
        self.main()


class Formula:

    def __init__(self, config: Config):
        self.pmin = int(config.get_info()[1])
        self.pmax = int(config.get_info()[0])

    def calculate_to(self, mark: float):
        answer = 1 + 3 * ((self.pmax - mark) / (self.pmax - self.pmin))
        if not 1 <= answer <= 6:
            return "∅"
        else:
            return float(str(answer)[:3])

    def calculate_from(self, mark: float):
        answer = -1 * (((mark - 1) * (self.pmax - self.pmin)) / 3 - self.pmax)
        return float(str(answer)[:5])


menu = Console()