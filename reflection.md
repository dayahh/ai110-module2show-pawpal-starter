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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
