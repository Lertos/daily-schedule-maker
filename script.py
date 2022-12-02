import calendar
from datetime import date
from fpdf import FPDF

output_path = r'C:\Users\Dylan\Downloads\schedule.pdf'
schedule_start_date = '2022-11-19'
schedule_end_date = '2023-02-07'

boxes = ['Workout', 'Read Book', 'Family', 'Friends', 'No Junk', 'Learning (45m+)', 'Project Work']

obj_calendar = calendar.Calendar()


class PDF(FPDF):
    
    header_size = 0
    normal_size = 0
    
    
    #Start Date: inclusive, End Date: exclusive
    def create_pdf(self, start_date, end_date):
        self.header_size = self.get_font_size(13)
        self.normal_size = self.get_font_size(9)
        
        dates = []
        
        start_date_obj = date.fromisoformat(start_date)
        end_date_obj = date.fromisoformat(end_date)
        
        start_year = start_date_obj.year
        end_year = end_date_obj.year
        
        if end_year < start_year:
            print('ERROR: End Year must be greater or equal to the Start Year')
            return
        elif start_year == end_year:
            dates = obj_calendar.yeardatescalendar(start_year, 1)
        else:
            for year in range(start_year, end_year + 1):
                year_calendar = obj_calendar.yeardatescalendar(year, 1)
                dates.append(year_calendar)
        
        current_dates = []

        for year in dates:
            for month in year:
                for week in month:
                    for day in week:
                        if type(day) == list:
                            for properDay in day:
                                if properDay < start_date_obj or properDay in current_dates:
                                    continue
                                elif properDay >= end_date_obj:
                                    break

                                formatted_date = date.strftime(properDay, '%a - %B %d, %Y')

                                self.record_for_date(formatted_date)
                                current_dates.append(properDay)
                        else:
                            if day < start_date_obj or day in current_dates:
                                continue
                            elif day >= end_date_obj:
                                break
                        
                            formatted_date = date.strftime(day, '%a - %B %d, %Y')

                            self.record_for_date(formatted_date)
                            current_dates.append(day)

                            #print(date.strftime(day, '%B %d, %Y'))

        
    def get_font_size(self, font_size):
        pdf.set_font('Arial', 'B', font_size)
        return pdf.get_string_width('T')
        
    
    def record_for_date(self, date):
        self.date_header(date)
        self.add_todo_list()

    
    def date_header(self, date):
        pdf.set_font('Arial', 'B', 13)

        width = pdf.get_string_width(date)
        pos_x = 210 - (width/2)

        pdf.cell(pos_x, h = 0, txt = date, border = 0, ln = 0, align = 'C')
        pdf.ln(self.header_size + 1)


    def add_todo_list(self):
        pdf.set_font('Arial', '', 9)
        
        size = self.normal_size * 2

        for box in boxes:
            pdf.rect(pdf.get_x(), pdf.get_y(), size, size)

            pdf.set_x(pdf.get_x() + size + 1)
            pdf.write(5, box)

            pdf.set_x(pdf.get_x() + size)
            
        self.add_solid_line(size)


    def add_solid_line(self, size):
        pdf.ln(size + 2)
        pdf.line(5, pdf.get_y(), 205, pdf.get_y())
        pdf.ln(self.header_size + 1)
            
            
pdf = PDF()
pdf.add_page()

#Start Date and End Date uses: YYYY-MM-DD
pdf.create_pdf(schedule_start_date, schedule_end_date)

pdf.output(output_path, 'F')
