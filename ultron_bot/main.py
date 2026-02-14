from ultron_bot.agent import UltronAgent
from ultron_bot.config import load_config
from ultron_bot.gui import UltronGUI


def main() -> None:
    config = load_config()
    agent = UltronAgent(config)
    app = UltronGUI(agent)
    app.run()


if __name__ == "__main__":
    main()
