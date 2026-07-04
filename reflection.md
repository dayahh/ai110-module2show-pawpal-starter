# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

User should be able to add themselves and a pet
User should be able to add a task and edit that task
User should be able to consider task priority

User Info class #to track name and info
- methods: add user, add pet
Pet Task class # pet specific tasks
- methods: add task, edit task, delete task
Task Schedule Class # scheduling tasks
- methods: add task to schedule
Daily Plan Class # care plan reccomendation
- methods: reccomendation of schedule

New refined classes:

Pet class # to track pet name and info
- methods: add pet, get tasks
Pet Task class # pet specific tasks
- methods: add task, edit task, delete task
Task Schedule class # scheduling tasks
- methods: add task to schedule
Daily Plan class # care plan recommendation
- methods: recommend schedule

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Design did change during implementation. Initially, I thought I needed an overall user class in order to define pets and then pet tasks. But I reread the prompt and it says only one user needs this software so I decided that removing the user class will make things clearer. More clarity came when I first gave my original classes to Claude and it looked very tricky and messy to follow, due to the methods it generated for me I believed it would be better to cut out the User class as a middleman, and it did agree with my assesment because it reduces the work being done.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
Priority — each task has a priority (1 = most important). DailyPlan.recommend_schedule() sorts by this, so important tasks get placed first.
Duration — duration_minutes determines how long a task occupies the day and is used to compute its end time.
Time / conflicts — TaskSchedule.add_task_to_schedule() checks whether a task's time range overlaps one already scheduled, using the start time + duration.
Preferred start time — in the app, each task can be given a specific time the owner wants it to happen.
Recurrence — daily/weekly tasks carry a frequency and due date, so completing one automatically schedules the next.

 I ranked constraints by how "breakable" they are. A time conflict makes the plan invalid, so it's non-negotiable; priority reflects the owner's intent, so it drives ordering; preferences are nice-to-have and yield when they collide with the hard rules


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The algo I reviewed was "create_next_occurrence"

The readability could be better because it is a lot of logic and a lot of lines for one simple method. Even I noticed a lot of the changes the AI wanted to add by creating several helper methods. We could have went with the helper method part but I didn't want to keep refactoring so early onn in this project. But so far there is no performance issue.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for all three. I was the main driver and used my brain to determine the main output, especially because the AI didn't have the full context of the homework. I decided what code outputs were too much for this simple project because it did try to go off the rails and add too much support. I found the prompts that were the most simple one liners got me the answers I need, especially when I asked the AI to clarify the choices it made. It's important to talk to the AI in a simple way so it does not misconstrue any needs of the project.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
Frequently I rejected the Ai suggestions. One recent example was expanding the scheduler. It tried to add a few helper methods and one method it claimed was optional, and that was getting to the point where I thought the AI was doing too much. I told it to just stick to one method we already had and refactor the lines from there. Personally I just think it can take the wheels and go wild if you don't give it the right structure.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

What I tested: the four core scheduling behaviors — task completion (mark_complete), task count increasing on add, priority ordering and chronological sorting, recurring-task spawning (daily creates the next day; one-time creates nothing), and time-conflict detection (overlapping tasks flagged and rejected, back-to-back allowed).

Why they mattered: these are the behaviors where a bug would break the app's whole purpose — a scheduler that double-books, mis-orders by priority, or silently drops recurring tasks is worse than none. I focused tests on the logic with real decisions (sorting, conflicts, recurrence) rather than simple data storage, since that's where mistakes actually hide.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I am confident my scheduler works because I perosnally have tested and reviewed the app myself. there were initial bugs that we went over together but those have been resolved after looking over the code again.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm really happy with the brainstorm part, I thought it was cool to take a critical step back, plan the basics and then expand from there if needed. The AI did a good job at supporting me on this stage and answered aquestions to come up with 4 good classes to use.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve the front end code, make the website look more cute!

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I think it's important to speak clearly every single time, and per prompt because this AI will take it's own choices and run with it before you know it. You have to be the architect of your own code even when some other thing is generating the code for you.