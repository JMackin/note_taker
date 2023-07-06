from dotenv import load_dotenv
from NoteTaker import orchestrate

load_dotenv()
orchestrator = orchestrate.Orchestrator()

orchestrator.build_jlmnote()
orchestrator.run_gui()
print(orchestrator.get_note_attrs()['content'])

