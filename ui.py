import tkinter as tk
from PIL import Image, ImageTk
import random

TRAVEL_TIPS = [
    "Travel Tip - Select Low-Impact Accommodations: Stay in eco-friendly or certified green hotels that prioritize sustainability in their operations.",
    "Travel Tip - Use Public Transport or Bike: Explore destinations by public transit, walking, or biking, rather than renting a car or using taxis.",
    "Travel Tip - Eat Local and Seasonal: Support local agriculture and reduce carbon emissions by choosing restaurants that serve local, seasonal dishes.",
    "Travel Tip - Carry Reusable Items: Pack a reusable water bottle, shopping bags, and utensils to minimize plastic waste.",
    "Travel Tip - Conserve Resources: Be mindful of your energy and water use in hotels. Turn off lights, reuse towels, and avoid long showers.",
    "Travel Tip -  Respect Natural Environments: Follow guidelines when visiting natural sites to minimize your impact on wildlife and habitats.",
    "Travel Tip - Educate Yourself on Local Cultures: Understand and respect the cultural practices and norms of the places you visit to foster positive interactions and reduce cultural impact.",
    "Travel Tip - Choose Sustainable Activities: Opt for eco-tourism experiences that promote conservation and benefit local communities.",
    "Travel Tip - Reduce, Reuse, Recycle: Always look for opportunities to reduce waste, reuse resources, and recycle when possible during your travels.",
    "Travel Tip - Support Eco-friendly Businesses: From tour operators to souvenir shops, prioritize spending your money with businesses that have sustainable practices."]


class VergeUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x700")
        self.answers = []

        self.original_image = Image.open("background.jpg")
        self.background_image = self.original_image.resize((1000, 700), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Set the image as the background
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.questions = ['Do you prefer a vacation in a climate that is primarily warm and sunny, rather than cold?',
                          'Would you like to be near beaches, lakes, rivers?',
                          'Are you looking for destinations where you can engage in outdoor activities, such as hiking,'
                          'skiing, or wildlife watching?',
                          'Do you prefer a destination that offers a vibrant nightlife?']

        self.question_index = 0

        self.label = tk.Label(master, text=self.questions[self.question_index], bg="light green", fg="black",
                              font=("Georgia", 15, "bold"))
        self.label.pack(pady=40)

        # Buttons
        self.yes_button = tk.Button(master, text="Yes", command=lambda: self.handle_answer("Yes"), font=("Georgia", 25),
                                    height=5, width=20)
        self.yes_button.pack(side=tk.LEFT, expand=True, padx=50, pady=20)

        self.no_button = tk.Button(master, text="No", command=lambda: self.handle_answer("No"), font=("Georgia", 25),
                                   height=5, width=20)
        self.no_button.pack(side=tk.RIGHT, expand=True, padx=50, pady=20)

    def handle_answer(self, answer):
        self.answers.append(answer)
        print(f"Answered {answer} to '{self.questions[self.question_index]}'")
        self.question_index += 1

        if self.question_index < len(self.questions):
            self.slide_transition()
        else:
            self.master.destroy()

    def show_next_question(self):
        self.transition_label.place_forget()
        self.label.config(fg="black")
        if self.question_index < len(self.questions):
            self.label.config(text=self.questions[self.question_index])
        else:
            self.master.destroy()

    def slide_transition(self):
        random_tip = random.choice(TRAVEL_TIPS)
        self.transition_label = tk.Label(self.master, text="Please wait as we prepare your next question \n\n" +
                                                           random_tip, bg="light green", fg="black",
                                                           font=("Georgia", 14))
        self.transition_label.place(x=-300, y=200)
        TRAVEL_TIPS.remove(random_tip)

        for x in range(-300, 101, 5):
            self.master.after(40, lambda x=x: self.transition_label.place(x=x, y=200))
            self.master.update_idletasks()
        self.master.after(7000, self.show_next_question)


def main():
    root = tk.Tk()
    app = VergeUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
