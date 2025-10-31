from crewai import Agent, Task, Crew
from textwrap import dedent

# 1️⃣ Define agents
greeter_agent = Agent(
    name="Greeter Agent",
    role="Friendly greeter",
    goal="Greet the user by name in a warm and friendly way.",
    backstory=dedent("""
        This agent specializes in personalized greetings.
        It always tries to sound cheerful and positive.
    """),
)

compliment_agent = Agent(
    name="Compliment Agent",
    role="Compliment generator",
    goal="Add a nice compliment to a given greeting.",
    backstory="Loves to make people smile.",
)

# 2️⃣ Define tasks (with input variables)
greet_task = Task(
    description="Greet the user whose name is {name}.",
    expected_output="A single-line friendly greeting using the name.",
    agent=greeter_agent,
)

compliment_task = Task(
    description="Take the greeting '{greeting}' and add a kind compliment.",
    expected_output="A friendly message with a compliment.",
    agent=compliment_agent,
)

# 3️⃣ Create the crew
crew = Crew(
    name="Greeting Crew",
    agents=[greeter_agent, compliment_agent],
    tasks=[greet_task, compliment_task],
)

# 4️⃣ Run the workflow with inputs
if __name__ == "__main__":
    inputs = {"name": "Joel"}  # 👈 dynamic user input
    result = crew.run(inputs=inputs)
    print("\nFinal Result:")
    print(result)

