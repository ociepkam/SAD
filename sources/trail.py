import time
import random
from os import listdir
from os.path import join
from psychopy import visual, event
from sources.check_exit import check_exit


class Trial:
    def __init__(self, win, config, item):
        images = [f for f in listdir(item)]

        taskA = [elem for elem in images if elem.split("_")[0][-1] == "A"][0]
        taskA = visual.ImageStim(win=win, image=join(item, taskA), interpolate=True,
                                 size=config['TASK_A_SIZE'], pos=config['TASK_A_POS'])

        taskB = [elem for elem in images if elem.split("_")[0][-1] == "B"][0]
        taskB = visual.ImageStim(win=win, image=join(item, taskB), interpolate=True,
                                 size=config['TASK_B_SIZE'], pos=config['TASK_B_POS'])

        answers = []
        elements = [elem for elem in images if elem.split("_")[0][-1] not in ["A", "B"]]
        random.shuffle(elements)

        for i, elem in enumerate(elements):
            pos_x = config['ANSWERS_POS'][0] - ((config["N_ANSWERS_IN_ROW"] - 1) / 2 - i % config["N_ANSWERS_IN_ROW"]) \
                    * (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][0])
            pos_y = config['ANSWERS_POS'][1] - i//config["N_ANSWERS_IN_ROW"] \
                    * (config["ANSWERS_SIZE"] + config["VIZ_OFFSET"][1])

            image = visual.ImageStim(win=win, image=join(item, elem), interpolate=True,
                                     size=config['ANSWERS_SIZE'], pos=[pos_x, pos_y])

            frame = visual.Rect(win, width=config["ANSWERS_SIZE"], height=config["ANSWERS_SIZE"],
                                pos=[pos_x, pos_y], lineColor="red")
            answers.append({"name": elem.split(".")[0].split("_", 2)[2], "image": image, "frame": frame})

        self.name = item
        self.taskA = taskA
        self.taskB = taskB
        self.answers = answers
        self.rt = None
        self.acc = None
        self.chosen_answer = None

    def setAutoDraw(self, draw, win):
        self.taskA.setAutoDraw(draw)
        self.taskB.setAutoDraw(draw)
        for elem in self.answers:
            elem["image"].setAutoDraw(draw)
        win.flip()

    def run(self, config, win, response_clock, clock_image, mouse, accept_box,
            feedback, feedback_positive, feedback_negative):
        accept_box.set_start_colors()
        win.callOnFlip(response_clock.reset)
        event.clearEvents()

        accept_box.setAutoDraw(True)
        self.setAutoDraw(True, win)
        clock_is_shown = False

        while response_clock.getTime() < config["STIM_TIME"]:
            for answer in self.answers:
                if mouse.isPressedIn(answer["frame"]):
                    for ans in self.answers:
                        ans["frame"].setAutoDraw(False)
                    answer["frame"].setAutoDraw(True)
                    self.chosen_answer = answer["name"]
                    self.acc = self.chosen_answer == "target_living"
                    print(self.acc)
                    accept_box.set_end_colors()
                    win.flip()
                    event.clearEvents()
                    break
            if mouse.isPressedIn(accept_box.accept_box) and self.chosen_answer is not None:
                self.rt = response_clock.getTime()
                break

            if not clock_is_shown and config["STIM_TIME"] - response_clock.getTime() < config["SHOW_CLOCK"]:
                clock_image.setAutoDraw(True)
                clock_is_shown = True
                win.flip()

            check_exit()
            win.flip()

        if feedback:
            print(self.answers)
            true_answer = str(self.answers.index([a for a in self.answers if a["name"] == "target_living"][0]) + 1)
            if self.acc:
                feedback_positive.text += true_answer
                feedback_positive.setAutoDraw(True)
                win.flip()
                time.sleep(config["FEEDBACK_SHOW_TIME"])
                feedback_positive.text = feedback_positive.text[:-len(true_answer)]
            else:
                feedback_negative.text += true_answer
                feedback_negative.setAutoDraw(True)
                win.flip()
                time.sleep(config["FEEDBACK_SHOW_TIME"])
                feedback_negative.text = feedback_negative.text[:-len(true_answer)]
            feedback_positive.setAutoDraw(False)
            feedback_negative.setAutoDraw(False)

        for ans in self.answers:
            ans["frame"].setAutoDraw(False)
        clock_image.setAutoDraw(False)
        accept_box.setAutoDraw(False)
        self.setAutoDraw(False, win)

    def info(self, exp, trial_nr):
        answers_order = [answer["name"] for answer in self.answers]
        #      ['TRIAL_NR', 'TASK_NR', 'EXPERIMENTAL', 'ACC',    'RT',     'ANSWER_TYPE',  'ANSWERS_ORDER']
        return [trial_nr,   self.name,      exp,      self.acc, self.rt, self.chosen_answer, answers_order]
