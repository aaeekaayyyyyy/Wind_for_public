# Wind Assistant

This project is a voice-activated assistant named Wind, designed to perform various tasks through speech recognition and command processing. It integrates with several services and functionalities, including Google Calendar, music playback, messaging, and system controls.

## Features

- **Voice Recognition**: Utilizes the `speech_recognition` library to listen for commands.
- **AI Processing**: Interacts with OpenAI's API to generate responses based on user input.
- **Calendar Management**: Allows users to add events and check their next scheduled event using Google Calendar.
- **Time Management**: Provides functionalities to tell the current time, set timers, and alarms.
- **System Controls**: Manages system settings such as volume, brightness, Wi-Fi, and Bluetooth.
- **Messaging**: Sends messages via WhatsApp.
- **Music Playback**: Controls music playback through Spotify.

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Wind
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Google Calendar API credentials:
   - Follow the instructions on the [Google Calendar API documentation](https://developers.google.com/calendar/quickstart/python) to create credentials and save them as `credentials.json` in the project directory.

4. Set your OpenAI API key in the `main.py` file.

## Usage

To run the assistant, execute the following command:
```
python main.py
```

Once running, you can activate the assistant by saying "hello" followed by your command. For example:
- "Open Google"
- "Set an alarm for 7 AM"
- "Send a message to John saying hello"

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.