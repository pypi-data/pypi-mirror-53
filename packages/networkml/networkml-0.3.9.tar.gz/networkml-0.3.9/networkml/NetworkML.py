import argparse
import fnmatch
import hashlib
import json
import logging
import os

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from networkml.algorithms.base import BaseAlgorithm
from networkml.utils.common import Common
from networkml.utils.model import Model


class NetworkML():
    """'
    Main class to run different algorithms against different network
    traffic data sources
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        self.args = None
        self.read_args()
        self.get_config()
        self.common = Common(config=self.config)
        self.logger = Common().setup_logger(self.logger)
        self.get_files()
        self.model_hash = None
        self.model = Model(duration=self.duration, hidden_size=None,
                           model_type=self.args.algorithm)
        if self.args.operation == 'eval':
            self.load_model()
            if self.args.algorithm == 'onelayer':
                BaseAlgorithm(files=self.files, config=self.config,
                              model=self.model, model_hash=self.model_hash, model_path=self.args.trained_model).eval(self.args.algorithm)
            elif self.args.algorithm == 'randomforest':
                BaseAlgorithm(files=self.files, config=self.config,
                              model=self.model, model_hash=self.model_hash, model_path=self.args.trained_model).eval(self.args.algorithm)
            elif self.args.algorithm == 'sos':
                from networkml.algorithms.sos.eval_SoSModel import eval_pcap
                eval_pcap(self.args.path, self.conf_labels, self.time_const)
        elif self.args.operation == 'train':
            if self.args.algorithm == 'onelayer':
                m = MLPClassifier(
                    (self.state_size),
                    alpha=0.1,
                    activation='relu',
                    max_iter=1000
                )
                BaseAlgorithm(files=self.files, config=self.config,
                              model=self.model, model_hash=self.model_hash,
                              model_path=self.args.trained_model).train(self.args.path, self.args.save, m, self.args.algorithm)
            elif self.args.algorithm == 'randomforest':
                m = RandomForestClassifier(
                    n_estimators=100,
                    min_samples_split=5,
                    class_weight='balanced'
                )
                BaseAlgorithm(files=self.files, config=self.config,
                              model=self.model, model_hash=self.model_hash,
                              model_path=self.args.trained_model).train(self.args.path, self.args.save, m, self.args.algorithm)
            elif self.args.algorithm == 'sos':
                from networkml.algorithms.sos.train_SoSModel import train
                train(self.args.path, self.time_const, self.rnn_size,
                      self.conf_labels, self.args.save)
        elif self.args.operation == 'test':
            self.load_model()
            if self.args.algorithm == 'onelayer':
                BaseAlgorithm(files=self.files, config=self.config,
                              model=self.model, model_hash=self.model_hash, model_path=self.args.trained_model).test(self.args.path, self.args.save)
            elif self.args.algorithm == 'randomforest':
                BaseAlgorithm(files=self.files, config=self.config,
                              model=self.model, model_hash=self.model_hash, model_path=self.args.trained_model).test(self.args.path, self.args.save)
            elif self.args.algorithm == 'sos':
                self.logger.info(
                    'There is no testing operation for the SoSModel.')

    def read_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--algorithm', '-a', default='onelayer',
                            choices=['onelayer', 'randomforest', 'sos'],
                            help='which algorithm to run')
        parser.add_argument('--format', '-f', default='pcap',
                            choices=['netflow', 'pcap'],
                            help='which format are the files to process in')
        parser.add_argument('--operation', '-o', default='eval',
                            choices=['eval', 'train', 'test'],
                            help='which operation to run')
        parser.add_argument('--trained_model', '-m', default='networkml/trained_models/onelayer/OneLayerModel.pkl',
                            help='path to the trained model file')
        parser.add_argument('--path', '-p', default='/pcaps',
                            help='path to file or directory of files to process')
        parser.add_argument('--save', '-w', default='networkml/trained_models/onelayer/OneLayerModel.pkl',
                            help='path to save the trained model, if training')

        self.args = parser.parse_args()
        return

    def get_files(self):
        # TODO checking extensions here should be moved to parsers, and it should probably use 'magic' rather than extensions
        self.files = []
        if Path(self.args.path).is_dir():
            for root, dirnames, filenames in os.walk(self.args.path):
                for extension in ['pcap', 'dump', 'cap']:
                    for filename in fnmatch.filter(filenames, '*.' + extension):
                        self.files.append(os.path.join(root, filename))
        elif Path(self.args.path).is_file() and \
                os.path.split(str(self.args.path))[-1].split('.')[-1] in {'pcap', 'dump', 'cap'}:
            self.files.append(str(self.args.path))
        else:
            self.logger.error(
                'Input \'%s\' was neither a file nor a directory.', str(self.args.path))

        if not self.files:
            self.logger.error(
                'Did not find file(s) from \'%s\'.', str(self.args.path))
        return

    def get_config(self, cfg_file='networkml/configs/config.json', labels_file='networkml/configs/label_assignments.json'):
        try:
            with open(cfg_file, 'r') as config_file:
                self.config = json.load(config_file)
            self.time_const = self.config['time constant']
            self.state_size = self.config['state size']
            self.look_time = self.config['look time']
            self.threshold = self.config['threshold']
            self.rnn_size = self.config['rnn size']
            self.duration = self.config['duration']
            #self.batch_size = self.config['batch size']
            with open(labels_file, 'r') as label_file:
                labels = json.load(label_file)
            self.conf_labels = []
            for label in labels:
                self.conf_labels.append(labels[label])
            self.conf_labels.append('Unknown')
            self.config['conf labels'] = self.conf_labels
        except Exception as e:  # pragma: no cover
            self.logger.error(
                "Unable to read '%s' properly because: %s", cfg_file, str(e))
        return

    def load_model(self):
        # Compute model hash
        with open(self.args.trained_model, 'rb') as handle:
            self.model_hash = hashlib.sha224(handle.read()).hexdigest()

        self.model.load(self.args.trained_model)
        self.logger.debug('Loaded model from %s', self.args.trained_model)
        return
