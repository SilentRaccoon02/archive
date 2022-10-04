using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using AngleSharp.Dom;
using AngleSharp.Html.Parser;
using Microsoft.EntityFrameworkCore;

namespace Project_1
{
    public static class TimetableTools
    {
        public static WeekTools Parse(string pageUri)
        {
            var parser = new HtmlParser();

            Console.WriteLine("request...");
            var page = GetPageAsync(pageUri).Result;
            var document = parser.ParseDocument(page);

            Console.WriteLine("parsing...");
            var weekParser = new WeekTools(document);
            return weekParser;
        }

        public static void ToDb(Week week)
        {
            Console.WriteLine("writing...");
            using var db = new TimetableContext();
            ((WeekTools) week).ToDb(db);
        }

        public static Week FromDb(string weekDate, string groupName)
        {
            using var db = new TimetableContext();

            var searchResult = db.Weeks
                .Include(b => b.WeekDate)
                .Include(b => b.GroupName)
                .Where(b => b.WeekDate.Date.Contains(weekDate))
                .Where(b => b.GroupName.Name.Contains(groupName))
                .Include(b => b.Days).ThenInclude(b => b.DayName)
                .Include(b => b.Days).ThenInclude(b => b.Subjects).ThenInclude(b => b.ClassTime)
                .Include(b => b.Days).ThenInclude(b => b.Subjects).ThenInclude(b => b.SubjectName)
                .Include(b => b.Days).ThenInclude(b => b.Subjects).ThenInclude(b => b.LecturerName)
                .Include(b => b.Days).ThenInclude(b => b.Subjects).ThenInclude(b => b.LocationName)
                .First();

            return searchResult;
        }

        private static async Task<string> GetPageAsync(string pageUri)
        {
            var client = new HttpClient();
            client.DefaultRequestHeaders.Add("Accept-Language", "ru");
            var response = await client.GetAsync(pageUri);
            response.EnsureSuccessStatusCode();
            var responseBody = await response.Content.ReadAsStringAsync();
            return responseBody;
        }
    }

    public class WeekTools : Week
    {
        public WeekTools(IParentNode document)
        {
            WeekDate = new WeekDate
            {
                Date = document.QuerySelector("div#timetable-week-navigator-chosen-week")?.QuerySelector("span")
                    ?.TextContent
            };

            GroupName = new GroupName
            {
                Name = document.QuerySelector(".col-sm-7")?.TextContent.Trim().Split(" ")[1]
            };

            var days = document.QuerySelector("div#accordion.panel-group")
                ?.QuerySelectorAll("div.panel.panel-default");

            Days = new List<Day>();

            foreach (var day in days)
            {
                Days.Add(new DayTools(day));
            }
        }

        public void ToDb(TimetableContext db)
        {
            var weekResult = db.Weeks
                .Include(b => b.WeekDate)
                .Include(b => b.GroupName)
                .Where(b => b.WeekDate.Date.Contains(WeekDate.Date))
                .Where(b => b.GroupName.Name.Contains(GroupName.Name));

            if (weekResult.Any())
            {
                Console.WriteLine("couple exists");
                return;
            }

            foreach (var day in Days)
            {
                ((DayTools) day).ToDb(db);
            }

            var weekDateResult = db.WeeksDates.Where(b => b.Date.Contains(WeekDate.Date));

            if (weekDateResult.Any())
            {
                WeekDateId = weekDateResult.First().Id;
            }
            else
            {
                db.WeeksDates.Add(WeekDate);
                db.SaveChanges();
                WeekDateId = WeekDate.Id;
            }

            WeekDate = null;

            var groupNameResult = db.GroupsNames.Where(b => b.Name.Contains(GroupName.Name));

            if (groupNameResult.Any())
            {
                GroupNameId = groupNameResult.First().Id;
            }
            else
            {
                db.GroupsNames.Add(GroupName);
                db.SaveChanges();
                GroupNameId = GroupName.Id;
            }

            GroupName = null;

            db.Weeks.Add(this);
            db.SaveChanges();
        }
    }

    public class DayTools : Day
    {
        public DayTools(IParentNode document)
        {
            var dayNameAndDate = document.QuerySelector("h4.panel-title")?.TextContent.Trim().Split(", ");

            Date = dayNameAndDate[1];

            DayName = new DayName
            {
                Name = dayNameAndDate[0]
            };

            var subjects = document.QuerySelector("ul.panel-collapse.nopadding.nomargin")?.QuerySelectorAll("li");

            Subjects = new List<Subject>();

            foreach (var subject in subjects)
            {
                Subjects.Add(new SubjectTools(subject));
            }
        }

        public void ToDb(TimetableContext db)
        {
            var isNew = false;

            foreach (var unused in Subjects.Where(subject => ((SubjectTools) subject).ToDb(db)))
            {
                isNew = true;
            }

            if (!isNew)
            {
                var firstSubjectResult = db.Subjects.Where(b => b.Id == Subjects.First().Id)
                    .Include(b => b.DaysSubjects).First();

                var firstSubjectDaysIds =
                    firstSubjectResult.DaysSubjects.Select(daySubject => daySubject.DayId).ToList();

                firstSubjectDaysIds.Sort();

                foreach (var subjectResult in Subjects.Select(subject =>
                    db.Subjects.Where(b => b.Id == subject.Id).Include(b => b.DaysSubjects).First()))
                {
                    if (firstSubjectResult.DaysSubjects.Count != subjectResult.DaysSubjects.Count)
                    {
                        isNew = true;
                        break;
                    }

                    var subjectDaysIds = subjectResult.DaysSubjects.Select(daySubject => daySubject.DayId).ToList();

                    subjectDaysIds.Sort();

                    if (firstSubjectDaysIds.Where((t, i) => t != subjectDaysIds[i]).Any())
                    {
                        isNew = true;
                    }

                    if (isNew)
                    {
                        break;
                    }
                }
            }

            var dayNameResult = db.DaysNames.Where(b => b.Name.Contains(DayName.Name));

            if (dayNameResult.Any())
            {
                DayNameId = dayNameResult.First().Id;
            }
            else
            {
                db.DaysNames.Add(DayName);
                db.SaveChanges();
                DayNameId = DayName.Id;
            }

            DayName = null;

            if (isNew)
            {
                var fullZeroCase = true;

                foreach (var unused in Subjects.Where(subject => subject.Id != 0))
                {
                    fullZeroCase = false;
                }

                if (!fullZeroCase)
                {
                    foreach (var subject in Subjects.Where(subject => subject.Id == 0))
                    {
                        db.Subjects.Add(subject);
                        db.SaveChanges();
                    }

                    isNew = false;
                }
            }

            if (isNew) return;
            {
                DaysSubjects = new List<DaySubject>();

                foreach (var subject in Subjects)
                {
                    DaysSubjects.Add(new DaySubject
                    {
                        SubjectId = subject.Id
                    });
                }

                Subjects = null;
            }
        }
    }

    public class SubjectTools : Subject
    {
        public SubjectTools(IParentNode document)
        {
            ClassTime = new ClassTime
            {
                Time = document.QuerySelector("div.col-sm-2.studyevent-datetime")?.QuerySelector("span")
                    ?.TextContent
                    .Trim().Replace((char) 8211, (char) 45)
            };

            SubjectName = new SubjectName
            {
                Name = document.QuerySelector("div.col-sm-4.studyevent-subject")?.QuerySelector("span")?.TextContent
                    .Trim()
            };

            LecturerName = new LecturerName
            {
                Name = document.QuerySelector("div.col-sm-3.studyevent-educators")?.QuerySelector("span")
                    ?.TextContent
                    .Trim()
            };

            LocationName = new LocationName
            {
                Name = document.QuerySelector("div.col-sm-3.studyevent-locations")?.QuerySelector("span")
                    ?.TextContent.Trim() ?? document.QuerySelector("div.col-sm-3.studyevent-multiple-locations")
                    ?.QuerySelector("span")?.TextContent.Trim()
            };
        }

        public bool ToDb(TimetableContext db)
        {
            var isNew = false;

            var classTimeResult = db.ClassesTimes.Where(b => b.Time.Contains(ClassTime.Time));

            if (classTimeResult.Any())
            {
                ClassTimeId = classTimeResult.First().Id;
            }
            else
            {
                db.ClassesTimes.Add(ClassTime);
                db.SaveChanges();
                ClassTimeId = ClassTime.Id;
                isNew = true;
            }

            ClassTime = null;

            var subjectNameResult = db.SubjectsNames.Where(b => b.Name.Contains(SubjectName.Name));

            if (subjectNameResult.Any())
            {
                SubjectNameId = subjectNameResult.First().Id;
            }
            else
            {
                db.SubjectsNames.Add(SubjectName);
                db.SaveChanges();
                SubjectNameId = SubjectName.Id;
                isNew = true;
            }

            SubjectName = null;

            var lecturerNameResult = db.LecturersNames.Where(b => b.Name.Contains(LecturerName.Name));

            if (lecturerNameResult.Any())
            {
                LecturerNameId = lecturerNameResult.First().Id;
            }
            else
            {
                db.LecturersNames.Add(LecturerName);
                db.SaveChanges();
                LecturerNameId = LecturerName.Id;
                isNew = true;
            }

            var locationNameResult = db.LocationsNames.Where(b => b.Name.Contains(LocationName.Name));

            if (locationNameResult.Any())
            {
                LocationNameId = locationNameResult.First().Id;
            }
            else
            {
                db.LocationsNames.Add(LocationName);
                db.SaveChanges();
                LocationNameId = LocationName.Id;
                isNew = true;
            }

            LecturerName = null;

            if (!isNew)
            {
                var subjectResult = db.Subjects
                    .Where(b => b.ClassTime.Id == ClassTimeId)
                    .Where(b => b.SubjectName.Id == SubjectNameId)
                    .Where(b => b.LecturerName.Id == LecturerNameId)
                    .Where(b => b.LocationName.Id == LocationNameId).Include(b => b.DaysSubjects);

                if (subjectResult.Any())
                {
                    Id = subjectResult.First().Id;
                }
                else
                {
                    isNew = true;
                }
            }

            LocationName = null;

            db.SaveChanges();

            return isNew;
        }
    }
}