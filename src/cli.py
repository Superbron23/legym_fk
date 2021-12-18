import os

from legym import *


class LegymCLI(LegymHacker):
    def __init__(self) -> None:
        super().__init__()
        print("------ 欢迎使用乐健命令行 ------")
        while not self.__cli_login():
            pass
        print("如果您是初次使用该应用，可以输入 `help` 来查看各命令使用方法。")

    def __valid_input(self, prompt: str = ">>> ") -> str:
        """Get non-empty user input.

        Args:
            prompt: Hint user what to do, default to '>>> '.

        Returns:
            Non-empty user input.
        """
        user_input = ""
        while user_input == "":
            user_input = input(prompt)
        return user_input

    def __cli_login(self) -> bool:
        """Show welcome to user at the beginning.

        Returns:
            `True` on success, or `False` on failure.
        """
        username = self.__valid_input("用户名：")
        password = self.__valid_input("密码：")
        try:
            name, school = self.login(username, password)
        except LegymException as e:
            print(e)
            return False
        else:
            print(f"{school}的{name}，欢迎回来！")
            return True

    def run(self) -> None:
        """Run CLI application."""
        while True:
            try:
                commands = self.__valid_input().split()
                if commands[0] == "login":
                    self.__parse_login(commands[1:])
                elif commands[0] == "reg":
                    self.__parse_reg(commands[1:])
                elif commands[0] == "sign":
                    self.__parse_sign()
                elif commands[0] == "act":
                    self.__parse_act(commands[1:])
                elif commands[0] == "run":
                    self.__parse_run(commands[1:])
                elif commands[0] == "help":
                    self.__parse_help(commands[1:])
                elif commands[0] == "quit":
                    self.__parse_quit()
                else:
                    print(f"不支持的命令：{commands[0]}")
            except LegymException as e:
                print(e)

    def __parse_reg(self, args: list) -> None:
        """Parse register command.

        Args:
            args: List containing activity to register.
        """
        if len(args) == 0:
            name, _, reason = self.sign_up()
            print(f"{name}：{reason}")
        else:
            for activity in args:
                name, _, reason = self.sign_up(activity)
                print(f"{name}：{reason}")

    def __parse_sign(self) -> None:
        """Parse sign command."""
        results = self.sign_in().items()
        print("\n".join([f"{result[0]}：{result[1]}" for result in results]))

    def __parse_act(self, args: list) -> None:
        """Parse activity command.

        Args:
            args: List containing activity category.
        """
        if len(args) == 0:
            self.__show_all_activities()
        else:
            state_name = args[0]
            state = (
                ActivityState.SIGNED
                if "signed".find(state_name) != -1
                else ActivityState.REGISTERED
                if "registered".find(state_name) != -1
                else ActivityState.AVAILABLE
                if "available".find(state_name) != -1
                else ActivityState.BLOCKED
                if "blocked".find(state_name) != -1
                else -1
            )
            if state == -1:
                print(f"类别不存在：{state_name}")
            else:
                self.__show_specified_activities(state)

    def __parse_run(self, args: list) -> None:
        """Parse help command.

        Args:
            args: List containing distance.
        """
        if len(args) == 0:
            distance, success = self.running()
        else:
            try:
                demand = float(args[0])
            except ValueError:
                demand = 0
            distance, success = self.running(demand)

        if success:
            print(f"成功上传跑步里程：{distance} km")
        else:
            print(f"上传失败！")

    def __parse_help(self, args: list) -> None:
        """Parse help command.

        Args:
            args: List containing the command to check out.
        """
        filename = "help" if len(args) == 0 else args[0]
        filepath = os.path.join("doc", f"{filename}.txt")
        try:
            with open(filepath, "r", encoding="utf-8") as fr:
                print(f"\n{fr.read()}\n")
        except FileNotFoundError:
            print(f"Document `{filename}` not found.")

    def __parse_quit(self) -> None:
        """Parse quit command."""
        print("------ 感谢支持 ------\n")
        exit(0)

    def __show_all_activities(self) -> None:
        """Show all activities."""
        print("已签到：")
        self.__show_specified_activities(ActivityState.SIGNED)
        print("\n已报名：")
        self.__show_specified_activities(ActivityState.REGISTERED)
        print("\n可报名：")
        self.__show_specified_activities(ActivityState.AVAILABLE)
        print("\n未开始：")
        self.__show_specified_activities(ActivityState.BLOCKED)

    def __show_specified_activities(self, state: int) -> None:
        """Show activities of specified state.

        Args:
            Specified state.
        """
        activities = list(
            filter(lambda activity: activity["state"] == state, self._activities)
        )
        print("\n".join([activity["name"] for activity in activities]))


if __name__ == "__main__":
    cli = LegymCLI()
    cli.run()