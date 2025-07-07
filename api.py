import io

from flask import Flask, request, make_response, send_file, Response
from .shared.constants import EXCEL_MIME
from .shared.models import Audio, Excel, Analysis
from .shared.services import Analysis as AnalysisService
from .shared.utils import is_excel, is_audio, save_file, save_new_file, file_dir

app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
    
def process_excel(file):
    if not is_excel(file):
       raise ValueError("Please check the excel's file type.")

    return Excel(file)

def process_audio(file):
    if not is_audio(file):
        raise ValueError("Please check the audio's file type: " + file.filename)

    return Audio(file, do_transcribe=True)  
    
def process_audios(files):
    successful = []
    failed = []
    
    for file in files:
        audio = process_audio(file)
        
        if audio.transcription is not None:
            successful.append(audio)
        else:
            failed.append(audio.filename)
            
    if not successful:
        raise ValueError("All audios failed processing.")
   
    return {
        "success": successful,
        "failed": failed
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'excel' not in request.files:
        return make_response("Please include an excel file.", 400)
    
    if 'audios' not in request.files:
        return make_response("Please include at least one audio file.", 400)
    
    try:
        excel = process_excel(request.files['excel'])
        audios = process_audios(request.files.getlist('audios'))
    except ValueError as e:
        return make_response(str(e), 400)
    
    result_http_code = 201

    if len(audios['failed']) > 0:
        result_http_code = 207
            
    analyzer = AnalysisService()
    
    excel.save()
    save_file(excel.file, app.root_path)

    for audio in audios['success']:
        audio.save()
        save_file(audio.file, app.root_path)
        
        # Analysis
        response = analyzer.analyze(audio.transcription)
        results = analyzer.match_entities(response, excel.fields)
        excel.populate_fields(results)

        analysis = Analysis.process(audio_filename=audio.filename, excel_filename=excel.filename, results=results)
        Analysis.get_db().addMany(analysis)
        
    output = io.BytesIO()
    excel.wb.save(output)
    output.seek(0)
    
    excel_path = save_new_file(output, excel.file.filename, app.root_path, temp=True)

    return make_response({
        "filename": excel.filename,
        "fields": excel.fields,
        "audios": [audio.to_dict() for audio in audios['success']],
        "excel": excel.format_content() # I'm sure there are better ways to display the excel data.
    }, result_http_code)

@app.route('/download', methods=['POST'])
def download():
    filename = request.form.get('filename')
    path = file_dir(filename, app.root_path, True)
    
    if not os.path.exists(path):
        return make_response("File doesn't exist", 404)
    
    response = send_file(path, mimetype=EXCEL_MIME)
    response.headers["Content-Name"] = filename
    
    return response
