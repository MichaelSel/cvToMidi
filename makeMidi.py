import json
import mido

def get_json(path):
    json_file = open(path)
    json_file = json_file.read()
    return json.loads(json_file)

dir = "C:/Users/Michael/PycharmProjects/similarity_analysis_py"
data = dir + "/analyzed/66_results_new.json"
all_midi_dir = "./midi"
all_subjects = get_json(data)

for s in all_subjects:
    if('blocks' not in s):continue
    if('SSS' not in s['id']):continue
    if('sets_to_exclude' in s): sets_to_exclude = s['sets_to_exclude']
    else: sets_to_exclude = []

    print(sets_to_exclude)
    # if('blocks' not in s):continue
    for block in s['blocks']:
        sub_dir = dir + "/data/" + s['id']
        block_num = block['block']
        for i,q in enumerate(block['similarity']):
            if(q['excluded']):
                #print("skipping question excluded")
                continue
            if (q['has_decoy']):
                #print("skipping question decoy")
                continue
            if (q['response'] == "neither"):
                #print("skipping neither")
                continue
            q_num = i
            order = q['order']
            probe_pitches = q['probe_pitches']
            swapped_pitches = q['swapped_pitches']
            shifted_pitches = q['shifted_pitches']
            pos = q['shift_position']
            set = ' '.join(str(e) for e in q['set'])
            set_str = ','.join(str(e) for e in q['set'])
            if(set_str in sets_to_exclude):
                # print("skipping question because it belongs to a set that was excluded")
                continue

            print(q['response'],pos)
            answer = q['response']

            #print(pitches, s['id'])
            # print(q)

            ## Makes midi file for probe
            tpb = 480
            file = mido.MidiFile(ticks_per_beat=tpb)
            track = file.add_track(name="melody")
            meta = mido.MetaMessage('set_tempo', tempo=333333)
            track.append(meta)
            for p in probe_pitches:
                start = 1
                end = tpb
                msg = mido.Message('note_on', note=60 + p, velocity=100, time=start)
                track.append(msg)
                msg = mido.Message('note_off', note=60 + p, velocity=100, time=end)
                track.append(msg)
            file.save(all_midi_dir + "/SUB-" + s['id'] + "-B-" + str(block_num) + "-Q-" + str(q_num) + "-type-probe-order-0-set-" + set + "-pos-na-resp-" + answer + ".mid")
            #

            ## Makes midi file for shifted
            tpb = 480
            file = mido.MidiFile(ticks_per_beat=tpb)
            track = file.add_track(name="melody")
            meta = mido.MetaMessage('set_tempo', tempo=333333)
            track.append(meta)
            for p in shifted_pitches:
                start = 1
                end = tpb
                msg = mido.Message('note_on', note=60+p, velocity=100, time=start)
                track.append(msg)
                msg = mido.Message('note_off', note=60+p, velocity=100, time=end)
                track.append(msg)
            file.save(all_midi_dir + "/SUB-" + s['id'] + "-B-" + str(block_num) + "-Q-" + str(q_num) + "-type-shifted-order-" + str(order.index('shifted')+1) + "-set-" + set + "-pos-" + str(pos) + "-resp-" + answer + ".mid")

            ## Makes midi file for swapped
            tpb = 480
            file = mido.MidiFile(ticks_per_beat=tpb)
            track = file.add_track(name="melody")
            meta = mido.MetaMessage('set_tempo', tempo=333333)
            track.append(meta)
            for p in swapped_pitches:
                start = 1
                end = tpb
                msg = mido.Message('note_on', note=60 + p, velocity=100, time=start)
                track.append(msg)
                msg = mido.Message('note_off', note=60 + p, velocity=100, time=end)
                track.append(msg)
            file.save(all_midi_dir + "/SUB-" + s['id'] + "-B-" + str(block_num) + "-Q-" + str(q_num) + "-type-swapped-order-" + str(order.index('swapped')+1) + "-set-" + set + "-pos-na-resp-" + answer + ".mid")

