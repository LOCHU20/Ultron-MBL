from ultron_bot.agent import UltronAgent
from ultron_bot.config import load_config
from ultron_bot.gui import UltronGUI
from ultron_bot.voice import VoiceEngine


def main() -> None:
    config = load_config()
    agent = UltronAgent(config)
    voice = VoiceEngine(tts_enabled=config.tts_enabled, stt_enabled=config.stt_enabled)
    app = UltronGUI(agent, voice)
    app = UltronGUI(agent)
    app.run()


if __name__ == "__main__":
    main()
