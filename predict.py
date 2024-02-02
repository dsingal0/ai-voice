from cog import BasePredictor, Input, Path
import os
from utils import (
    download_online_model,
    generate_ai_cover,
    get_video_length,
    convert_to_wav,
)
import os
from r8_utils import maybe_download_with_pget, delay_prints
import tarfile


class Predictor(BasePredictor):
    @staticmethod
    def untar_all(src_dir, output_dir):
        # create output_dir if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Get a list of all tar files in the source directory
        tar_files = [f for f in os.listdir(src_dir) if f.endswith(".tar")]
        # copy non tar files to output directory
        for file in os.listdir(src_dir):
            if not file.endswith(".tar"):
                os.system(f"mv {os.path.join(src_dir, file)} {output_dir}")
        # Untar each tar file
        for tar_file in tar_files:
            input_path = os.path.join(src_dir, tar_file)
            output_path = os.path.join(output_dir, os.path.splitext(tar_file)[0])

            with tarfile.open(input_path, "r") as tar:
                tar.extractall(output_path)

    def setup(self):
        remote_filenames = []
        # get rvc and mdxnet models
        # get rvc models
        with open("MANIFEST_1.txt", "r") as manifest_file:
            for line in manifest_file:
                remote_filenames.append(line.strip())
        print(remote_filenames)
        # print(remote_filenames)
        maybe_download_with_pget(
            path=os.path.join(os.getcwd(), "rvc_models_tar"),
            remote_path="https://weights.replicate.delivery/wqzt/e6e7f6d6-3c87-459a-8399-8758391ea705/rvc_models_tar",
            remote_filenames=remote_filenames,
        )
        remote_filenames = []
        # untar all the files
        self.untar_all(
            os.path.join(os.getcwd(), "rvc_models_tar"),
            os.path.join(os.getcwd(), "rvc_models"),
        )
        # detele the tar files
        #for file in os.listdir(os.path.join(os.getcwd(), "rvc_models_tar")):
        #    os.remove(os.path.join(os.getcwd(), "rvc_models_tar", file))

        # get mdxnet models
        with open("MANIFEST_2.txt", "r") as manifest_file:
            for line in manifest_file:
                remote_filenames.append(line.strip())
        print(remote_filenames)
        # print(remote_filenames)
        maybe_download_with_pget(
            path=os.path.join(os.getcwd(), "mdxnet_models"),
            remote_path="https://weights.replicate.delivery/wqzt/e6e7f6d6-3c87-459a-8399-8758391ea705/mdxnet_models",
            remote_filenames=remote_filenames,
        )

    @delay_prints(REALLY_EAT_MY_PRINT_STATEMENTS=True)
    def predict(
        self,
        voice_model: str = Input(
            description="Voice model.",
            choices=[
                "custom",
                "2pac",
                "adele",
                "alvin",
                "ariana-grande",
                "avril-lavigne",
                "baby",
                "ballin",
                "biden",
                "billie-eilish",
                "britney-spears",
                "camila-cabello",
                "chester-bennington",
                "chris-martin",
                "craig-tucker",
                "darthvader",
                "dio",
                "drake",
                "elon-musk",
                "elvis-presley",
                "eminem",
                "eric-cartman",
                "frank-sinatra",
                "freddie-mercury",
                "gojo",
                "goku",
                "hatsune-miku",
                "homer",
                "inosuke-hashibira",
                "janis-joplin",
                "justin-beiber",
                "kanao-tsuyuri",
                "kanye",
                "kimberly-loaiza",
                "kurt-cobain",
                "lady-gaga",
                "lisa-simpsons",
                "luffy",
                "megan-thee-stallion",
                "megatron",
                "michael-jackson",
                "miley-cyrus",
                "mordecai",
                "morgan-freeman",
                "mrbeast",
                "mrkrabs",
                "mrohare",
                "nami",
                "naruto",
                "neco-arc",
                "nezuko-kamado",
                "nicki-minaj",
                "nico-robin",
                "obama",
                "paul-mccartney",
                "peter-griffin",
                "pikachu",
                "plankton",
                "rihanna",
                "ronaldo",
                "roronoa-zoro",
                "sammy-hagar",
                "sanji",
                "selena-gomez",
                "siri",
                "spongebob-squarepants",
                "squidward",
                "stewie-griffin",
                "tanjiro-kamado",
                "tate",
                "taylor-swift",
                "the-weeknd",
                "toad",
                "toothbrush",
                "travis-scott",
                "trump",
                "villager",
                "xxxtentacion",
                "zenitsu-agatsuma",
            ],
            default="taylor-swift",
        ),
        audio: Path = Input(
            description="song_input",
            default=None,
        ),
        youtube_link: str = Input(
            description="Youtube link.",
            default=None,
        ),
        custom_voice_model_link: str = Input(
            description="Custom voice model link.", default=None
        ),
    ) -> Path:
        if audio and youtube_link:
            raise (Exception("Choose audio or youtube link."))
        if audio:
            if audio.as_posix().endswith(".mp3"):
                audio = Path(convert_to_wav(audio.as_posix()))
        if youtube_link:
            audio = youtube_link
            if get_video_length(youtube_link) > 300:
                raise Exception("Video length should be 5 minutes or less.")
        if voice_model == "custom":
            download_online_model(custom_voice_model_link)
            generate_ai_cover(audio, "custom")
            # delete created files
            os.remove(audio)
            return Path("song_output/output.mp3")

        generate_ai_cover(audio, voice_model)
        return Path("song_output/output.mp3")
