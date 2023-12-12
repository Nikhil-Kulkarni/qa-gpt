# QA GPT

One of the most painful and ignored parts of software development is thorough testing. Sure, great engineers will write unit tests & integration tests. Some might even write UI tests. But if you're lazy like me, you tend to be a little lackadaisical when it comes to testing your product with the user in mind. A quote I've frequently heard is "That's the QA team's job" when it comes to functionality testing.

I made QA GPT to help engineers & QA teams test the functionality of their products without writing any code and without spending already constrained human time doing functionality tests.

Here's a short demo video showing how it works:

https://nucleus-form.s3.us-west-2.amazonaws.com/Screen+Recording+2023-12-07+at+10.53.23+PM.mov

## Running QA GPT

Running QA GPT is remarkably simple, as it's just a simple python project. Note that you must have access to GPT-4-Vision in order to be able to run QA GPT. To run the project:

1. Get your GPT-4-Vision enabled API key from OpenAI
2. Drop the key into the `OPENAI_API_KEY` environment variable
3. Open `main.py` and change the `task` and url in the initial `driver.navigate` to match your test case
4. Run `python main.py`

I've included an example testing task in `main.py` that logs into a website with the given credentials, makes a change to an input field, saves it, and verifies that it was successfully saved. Feel free to modify the task and url as you wish to fit your test case.

## Roadmap

- [x] Use GPT-4 Vision to automate browser actions
- [x] Basic actions like click + fill in an input field
- [x] Prompt engineering to make it recognize when things go wrong
- [x] Log stack traces and record sessions
- [ ] Drag and drop action
- [ ] Map stack traces to timestamps in video recordings
- [ ] A clean UI to view the video recordings + see stack traces
- [ ] Plug into CI tools for continuous runs on every commit to the master branch
- [ ] Chain prompts for deeper understanding of failures
- [ ] Alerting into Slack when errors come up
- [ ] Plugin LlaVa and CogVLM to make the AI cheaper + faster
- [ ] Write better comments + make a Youtube explainer.
- [ ] Introduce a hosted solution

## Acknowledgements

- [https://github.com/ishan0102/vimGPT](https://github.com/ishan0102/vimGPT). The entire vision module + usage of Vimium is basically copied from Ishan's repo.
- [https://github.com/nat/natbot](https://github.com/nat/natbot). This gave me inspiration in the first place to use Generative AI for testing automation
