using System;

namespace Project_1
{
    internal static class Program
    {
        private static void Main(string[] args)
        {
            const string pageUri1 = "https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/303077/2021-11-08";
            const string pageUri2 = "https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/303077/2021-11-15";

            var week1FromUri = TimetableTools.Parse(pageUri1);
            TimetableTools.ToDb(week1FromUri);

            var week2FromUri = TimetableTools.Parse(pageUri2);
            TimetableTools.ToDb(week2FromUri);

            var week1FromDb = TimetableTools.FromDb("8 ноября – 14 ноября", "20.Б07-пу");
            Console.WriteLine("\n" + week1FromDb + "\n");

            var week2FromDb = TimetableTools.FromDb("15 ноября – 21 ноября", "20.Б07-пу");
            Console.WriteLine("\n" + week2FromDb + "\n");
        }
    }
}