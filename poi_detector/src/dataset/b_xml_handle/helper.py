import csv
from .constants_dataset import csv_dir
import urllib.parse


def remove_empty_lines(csv_path):
    with open(csv_path, "r") as csv_file:
        lines = csv_file.readlines()
    new_lines = []
    for line in lines:
        if line != '\n':
            new_lines.append(line)

    with open(csv_path, "w") as csv_file:
        csv_file.writelines(new_lines)


""" ALL BELOW ---> REKORDBOX XML """


def read_pois(track):
    frames = []
    for section in track:
        if section.tag == 'POSITION_MARK':
            t = float(section.attrib['Start'])
            frames.append(t)

    return frames


def decode(url_string):
    """ This function takes an unquoted url-string and returns the filename in the end of it. """
    decoded = urllib.parse.unquote(url_string)
    url_object = urllib.parse.urlparse(decoded)
    path = url_object.path
    filename = path[path.rfind('/') + 1:]
    return filename


def write_on_csv(fname, point_list, filewriter):
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


def create_csv_vdj(dj_playlists, xml_name):
    counter = 0
    csv_name = xml_name.replace('xml', 'csv')
    with open(csv_dir + csv_name, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for field in dj_playlists:

            for track in field:
                point_list = read_pois(track)

                url = track.attrib['Location']
                fname = decode(url)

                counter += write_on_csv(fname, point_list, filewriter)

    print('\nNumber of songs with POIs:')
    print('\t' + str(counter))


def create_csv_rekordbox(dj_playlists, xml_name):
    counter = 0
    csv_name = xml_name.replace('xml', 'csv')
    with open(csv_dir + csv_name, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for field in dj_playlists:

            if field.tag == 'COLLECTION':

                for track in field:
                    point_list = read_pois(track)

                    url = track.attrib['Location']
                    fname = decode(url)

                    counter += write_on_csv(fname, point_list, filewriter)

    print('\nNumber of songs with POIs:')
    print('\t' + str(counter))
