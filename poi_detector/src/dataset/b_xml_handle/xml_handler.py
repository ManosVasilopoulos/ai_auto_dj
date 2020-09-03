import urllib.parse
import csv

csv_dir = 'D:/Documents/Thesis/Project Skaterbot/Datasets/CSV/'


class rekordbox_xml_handler:
    def create_csv(self, dj_playlists, xml_name):
        counter = 0
        csv_name = xml_name.replace('xml', 'csv')
        with open(csv_dir + csv_name, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for field in dj_playlists:

                if field.tag == 'COLLECTION':
                    for track in field:
                        point_list = self.__read_pois(track)

                        url = track.attrib['Location']
                        fname = self.__get_file_name(url)
                        counter += self.__write_on_csv(fname, point_list, filewriter)

            print('\nNumber of songs with POIs:')
            print('\t' + str(counter))

    def __remove_empty_lines(self, csv_path):
        with open(csv_path, "r") as csv_file:
            lines = csv_file.readlines()
        new_lines = []
        for line in lines:
            if line != '\n':
                new_lines.append(line)

        with open(csv_path, "w") as csv_file:
            csv_file.writelines(new_lines)

    """ ALL BELOW ---> REKORDBOX XML """

    def __read_pois(self, track):
        frames = []
        for section in track:
            if section.tag == 'POSITION_MARK':
                t = float(section.attrib['Start'])
                frames.append(t)

        return frames

    def __get_file_name(self, url_string):
        """ This function takes an unquoted url-string and returns the filename in the end of it. """
        decoded = urllib.parse.unquote(url_string)
        url_object = urllib.parse.urlparse(decoded)
        path = url_object.path
        filename = path[path.rfind('/') + 1:]
        return filename

    def __write_on_csv(self, fname, point_list, filewriter):
        if point_list:
            print('Putting: ' + fname)
            filewriter.writerow([fname, point_list])
            filewriter.writerow([fname.replace('.wav', '-pitch-6.wav'), point_list])
            filewriter.writerow([fname.replace('.wav', '-pitch--6.wav'), point_list])
            filewriter.writerow([fname.replace('.wav', '-pitch-3.wav'), point_list])
            filewriter.writerow([fname.replace('.wav', '-pitch--3.wav'), point_list])
            filewriter.writerow([
                fname.replace('.wav', '-stretch0.75.wav'),
                list(map(lambda x: x / 0.75, point_list))
            ])
            filewriter.writerow([
                fname.replace('.wav', '-stretch1.25.wav'),
                list(map(lambda x: x / 1.25, point_list))
            ])
            return 1
        else:
            print('|\n    Skipping: ' + fname + '|\n')
            return 0


class vdj_xml_handler:
    directory = 'D:\\Documents\\Thesis\\Cue Point Detection Dataset\\'
    mode_list = ['', '-pitch-3', '--pitch-3', '-pitch-6', '--pitch-6', '-stretch0.75', '-stretch1.25']

    def create_csv(self, vdj_database, xml_name):
        counter = 0
        csv_name = xml_name.replace('xml', 'csv')
        with open(csv_dir + csv_name, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for track in vdj_database:
                if track.tag == 'Song':

                    fname = track.attrib['FilePath']
                    print('Calculating for: ' + fname)
                    point_list = self.__read_pois(track, fname)

                    if point_list != []:
                        fname = fname.replace(self.directory, '')
                        fname = fname.replace('.mp3', '')
                        fname = fname.replace('.Mp3', '')
                        fname = fname.replace('.MP3', '')
                        counter += self.__write_on_csv(fname, point_list, filewriter)

            print('\nNumber of songs with POIs:')
            print('\t' + str(counter))

    def __write_on_csv(self, fname, point_list, filewriter):
        if point_list:
            filewriter.writerow([fname + '.wav', point_list])
            filewriter.writerow([fname + '-pitch-6.wav', point_list])
            filewriter.writerow([fname + '-pitch--6.wav', point_list])
            filewriter.writerow([fname + '-pitch-3.wav', point_list])
            filewriter.writerow([fname + '-pitch--3.wav', point_list])
            filewriter.writerow([
                fname + '-stretch0.75.wav',
                list(map(lambda x: x / 0.75, point_list))
            ])
            filewriter.writerow([
                fname + '-stretch1.25.wav',
                list(map(lambda x: x / 1.25, point_list))
            ])
            return 1
        else:
            print('|\n    Skipping: ' + fname + '|\n')
            return 0

    def __read_pois(self, track, fname):
        frames = []
        for section in track:
            if section.tag == 'Poi':
                if 'Type' in section.attrib:
                    if section.attrib['Type'] == 'cue':
                        try:
                            t = float(section.attrib['Pos']) * 1000
                        except:
                            print(section.attrib)
                            raise Exception('-----------------------')
                        t = round(t) / 1000

                        try:
                            frames.append(t)
                        except Exception as e:
                            print('vdj_xml_handler: ' + str(e) + '\n' + fname)
                            break
        return frames
