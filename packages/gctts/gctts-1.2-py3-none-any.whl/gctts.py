import requests
import base64
import json
import click
import os

class googleTTS:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def _makePostRequest(self, endpoint, payload):
        url = f"https://texttospeech.googleapis.com/v1/{endpoint}"
        querystring = {"key": f"{self.apiKey}"}
        headers = {"content-type": "application/json"}
        r = requests.request(
            "POST", url, data=payload, headers=headers, params=querystring
        )

        if r.status_code == requests.codes.ok:
            return r.json()
        elif (
            r.json()["error"] is not "null"
            and r.json()["error"]["message"].find("API key not valid") != -1
        ):
            raise ValueError("Invalid API Key. Did you specify one with --apikey?")

    def _decodeB64Mp3(self, data):
        return base64.b64decode(data)

    def writeMp3toFile(self, dataBytes, path):
        with open(path, "wb") as file:
            file.write(dataBytes)

    def generateMp3(self, voice, language, string, speakingRate):
        payload = json.dumps(
            {
                "voice": {"name": voice, "languageCode": language},
                "input": {"text": string},
                "audioConfig": {"audioEncoding": "mp3", "speakingRate": speakingRate},
            }
        )

        reqObj = self._makePostRequest("text:synthesize", payload)
        return self._decodeB64Mp3(reqObj["audioContent"])


@click.group()
def cli():
    pass


@click.command()
@click.option("--apikey", envvar="GCTTS_APIKEY", help="Google Cloud API key that has acceess to Cloud TTS.",)
@click.option("--voice", default="en-US-Wavenet-F", help="The Google TTS voice.")
@click.option("--language", default="en-US", help="The langage the voice should be created in.")
@click.option("--rate", default=1.00, help="The speed in which the voice speaks.")
@click.option("--text", prompt="Text", help="Text that should be spoken.")
@click.argument("filename")
def mp3(apikey, voice, language, rate, text, filename):
    click.echo(
        "This script nor the developer (JamesClick) are not fuffiliated with Google whatsoever."
    )
    dirpath = os.getcwd()

    ttsInst = googleTTS(apikey)
    try:
        mp3Obj = ttsInst.generateMp3(voice, language, text, str(rate))
        with open(os.path.join(os.getcwd(), filename), "wb") as file:
            file.write(mp3Obj)
    except ValueError as error:
        click.echo(f"ERROR: {error}")


cli.add_command(mp3)

if __name__ == "__main__":
    cli()
