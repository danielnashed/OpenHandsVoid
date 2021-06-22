import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from .base import BaseIsolatedDataset

class GSLDataset(BaseIsolatedDataset):

    def read_index_file(self, index_file_path, splits):
        # `splits` is pointless here as we pass the split-specific CSV directly
        # CSV Columns: (video_path, gloss_name)
        df = pd.read_csv(index_file_path, delimiter='|', header=None)

        self.glosses = [df[1][i].strip() for i in range(len(df))]
        label_encoder = LabelEncoder()
        label_encoder.fit(self.glosses)

        for i in range(len(df)):
            gloss_cat = label_encoder.transform([df[1][i]])[0]
            instance_entry = df[0][i], gloss_cat
            self.data.append(instance_entry)

    def read_data(self, index):
        video_name, label = self.data[index]
        video_path = os.path.join(self.root_dir, video_name)
        imgs = self.load_frames_from_folder(video_path)
        if imgs is None:
            # Some folders don't have images in ".jpg" extension.
            imgs = self.load_frames_from_folder(video_path, pattern="glosses*")
            if not images:
                exit(f"No images in {video_path}")
        return imgs, label, video_name