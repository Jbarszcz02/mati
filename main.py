import customtkinter, subprocess
from CTkMessagebox import CTkMessagebox
import threading
class Gui(customtkinter.CTk):  
    def __init__(self): 
        super().__init__()  # Stworzenie głównego okienka
        self.title(".DAV to .MP4")
        self.geometry("740x400")
        self._set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")
        self.buttons()
        self.labels()
        self.check_ffmpeg()
        self.file_path = None 
        self.save_path = None 
        self.segmented_button_creation()
        
        
    
    def buttons(self): # Przyciski
        self.button = customtkinter.CTkButton(self, text="Wybierz plik", command=self.file_open)
        self.button.place(x=60, y=50)
        self.button3 = customtkinter.CTkButton(self, text="Zapisz plik", command=self.file_save)
        self.button3.place(x=60, y=150)
        self.button2 = customtkinter.CTkButton(self, text="Konwertuj do MP4",width=30 ,command= self.convert_command) 
        self.button2.place(x=60, y=350)
        self.button4 = customtkinter.CTkButton(self,text="Info", width=30,command= lambda: CTkMessagebox(title="Typy konwersji", width=520, message="Konwersja szybka - Błyskawiczna konwersja nagrania, możliwa utrata danych w trakcie.\n\nKonwersja wolna - Powolna, ale dokładna konwersja nagrania."))
        self.button4.place(x=300, y=253)
        self.button5 = customtkinter.CTkButton(self,text="Anuluj", width=30,command=self.cancel)     
         
    
        
    def labels(self): # Etykiety
        self.label= customtkinter.CTkLabel(self, width=400)
        self.label.place(x=210, y=50)
        self.label.configure(text="Nie wybrano pliku")
        self.label1= customtkinter.CTkLabel(self, width=400)
        self.label1.place(x=210, y=150)
        self.label1.configure(text="Nie wybrano miejsca zapisu")
        self.label2=customtkinter.CTkLabel(self, width=40)
        self.label2.place(x=400, y=350)
        self.label2.configure(text="")
        self.label3 =customtkinter.CTkLabel(self, width=740, height=40)
        self.label3.place(x=0, y=0)
        self.label3.configure(text="")
        
    def file_open(self): # Okienko wyboru plików .DAV
        file = customtkinter.filedialog.askopenfile(defaultextension=".dav", filetypes=[("dav", ".dav")])
        if file:
            self.file_path = file.name
            self.label.configure(text=self.file_path)
            self.label2.configure(text="")
    
    def file_save(self): # Okienko zapisu pliku w formacie .MP4
        save = customtkinter.filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("mp4","*.mp4")])
        if save:
            self.save_path = save
            self.label1.configure(text=self.save_path)
            
        
      
    def segmented_button_callback(self, value): #Przypisanie komendy po wybrananiu opcji
        if value == "Konwersja szybka":
            self.cnv = ['powershell.exe', "ffmpeg","-fflags","+igndts", "-i", self.file_path,"-map 0:0?","-map 0:1?","-map 0:2?", "-c:v", "copy", "-c:a", "copy","-vsync passthrough", self.save_path]
            self.label2.configure(text="")
        elif value == "Konwersja wolna":
            self.cnv = ['powershell.exe', "ffmpeg","-fflags","+igndts", "-i", self.file_path,"-map 0:0?","-map 0:1?","-map 0:2?", "-c:v libx264", "-vsync passthrough", self.save_path]
            self.label2.configure(text="")
            
    
    def segmented_button_creation(self): #Przycisk segmentowany z dwiema opcjami 
        self.seg_but = customtkinter.CTkSegmentedButton(self, height=35, width=500, values= ["Konwersja szybka", "Konwersja wolna"], command=self.segmented_button_callback)
        self.seg_but.place(x=60, y=250)
    
    def convert_command(self): #Konwertowanie - komendy + komunikaty

        self.label2.configure(text="Konwersja w trakcie")
        self.button5.place(x=200, y=350)
        self.button2.configure(state="disabled")
        self.seg_but.configure(state="disabled")
        self.button.configure(state="disabled")
        self.button3.configure(state="disabled")
        self.button4.configure(state="disabled")
        
        
        
        
        
        

        def run_conversion():
            k=subprocess.run(self.cnv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)
            if k.returncode == 0:
                u = subprocess.run(['powershell','echo', 'Done!'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)
                if "Done!" in u.stdout:
                    self.label2.configure(text="Konwersja zakończona")
                    CTkMessagebox(title=".DAV to .MP4", message="Konwersja przebiegła pomyślnie", icon="check")
                    

            
            
                
    
        thread = threading.Thread(target=run_conversion)
        thread.start()

    def cancel(self):
        
        subprocess.run(['powershell.exe', "TaskKill", "/im", "ffmpeg.exe", "/F"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        self.output= subprocess.run(['powershell.exe', 'echo', 'canceled'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        self.button5.place_forget()
        self.button2.configure(state="normal")
        self.seg_but.configure(state="normal")
        self.button.configure(state="normal")
        self.button3.configure(state="normal")
        self.button4.configure(state="normal")
        self.label2.configure(text="Konwersja przerwana")
        CTkMessagebox(title=".DAV to .MP4", message="Konwersja została przerwana", icon="cancel")
        
              
    
    def check_ffmpeg(self): # Sprawdzanie obecności ffmpeg z komunikatem
         self.chk1=subprocess.run(['powershell.exe', "ffmpeg", "-version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
         if "ffmpeg version" in self.chk1.stdout:
            pass
         else:
            self.label3.configure(text="Nie posiadasz ffmpeg, skontaktuj się z IT", fg_color="red", text_color="black", font=('',18))
             
    

gui = Gui()
gui.check_ffmpeg()
gui.mainloop()