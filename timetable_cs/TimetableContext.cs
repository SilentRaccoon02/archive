using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.EntityFrameworkCore;

namespace Project_1
{
    public class DayName
    {
        public int Id { get; set; }

        public string Name { get; set; }
    }

    public class ClassTime
    {
        public int Id { get; set; }

        public string Time { get; set; }
    }

    public class SubjectName
    {
        public int Id { get; set; }

        public string Name { get; set; }
    }

    public class LecturerName
    {
        public int Id { get; set; }

        public string Name { get; set; }
    }

    public class LocationName
    {
        public int Id { get; set; }

        public string Name { get; set; }
    }

    public class Subject
    {
        public int Id { get; set; }

        public int ClassTimeId { get; set; }

        public ClassTime ClassTime { get; set; }

        public int SubjectNameId { get; set; }

        public SubjectName SubjectName { get; set; }

        public int LecturerNameId { get; set; }

        public LecturerName LecturerName { get; set; }

        public int LocationNameId { get; set; }

        public LocationName LocationName { get; set; }

        public List<Day> Days { get; set; }
        public List<DaySubject> DaysSubjects { get; set; }

        public override string ToString()
        {
            var locationName = LocationName.Name == "С использованием информационно-коммуникационных технологий"
                ? "дистант"
                : "очно";
            var lecturerName = LecturerName.Name.Length < 20 ? $", {LecturerName.Name}" : "";

            return $"({ClassTime.Time}, {locationName}) {SubjectName.Name}{lecturerName}";
        }
    }

    public class DaySubject
    {
        public int DayId { get; set; }

        public Day Day { get; set; }

        public int SubjectId { get; set; }

        public Subject Subject { get; set; }
    }

    public class Day
    {
        public int Id { get; set; }

        public string Date { get; set; }

        public int DayNameId { get; set; }

        public DayName DayName { get; set; }

        public List<Subject> Subjects { get; set; }

        public List<Week> Weeks { get; set; }

        public List<DaySubject> DaysSubjects { get; set; }

        public override string ToString()
        {
            var outString = $"{DayName.Name}, {Date}\n";

            return Subjects.Aggregate(outString, (current, subject) => current + $"{subject}\n");
        }
    }

    public class WeekDate
    {
        public int Id { get; set; }

        public string Date { get; set; }
    }

    public class GroupName
    {
        public int Id { get; set; }

        public string Name { get; set; }
    }

    public class Week
    {
        public int Id { get; set; }

        public int WeekDateId { get; set; }

        public WeekDate WeekDate { get; set; }

        public int GroupNameId { get; set; }

        public GroupName GroupName { get; set; }

        public List<Day> Days { get; set; }

        public override string ToString()
        {
            var outString = $"{WeekDate.Date}, {GroupName.Name}\n";

            return Days.Aggregate(outString, (current, day) => current + $"{day}\n")[..^2];
        }
    }

    public class TimetableContext : DbContext
    {
        public DbSet<ClassTime> ClassesTimes { get; set; }

        public DbSet<SubjectName> SubjectsNames { get; set; }

        public DbSet<LecturerName> LecturersNames { get; set; }

        public DbSet<LocationName> LocationsNames { get; set; }

        public DbSet<Subject> Subjects { get; set; }

        public DbSet<DayName> DaysNames { get; set; }

        public DbSet<Day> Days { get; set; }

        public DbSet<WeekDate> WeeksDates { get; set; }

        public DbSet<GroupName> GroupsNames { get; set; }

        public DbSet<Week> Weeks { get; set; }

        private string DbPath { get; }

        public TimetableContext()
        {
            var path = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            DbPath = $"{path}{System.IO.Path.DirectorySeparatorChar}timetable.db";
        }

        protected override void OnConfiguring(DbContextOptionsBuilder options)
        {
            options.UseSqlite($"Data Source={DbPath}");

            options.EnableSensitiveDataLogging();
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Day>()
                .HasMany(b => b.Subjects)
                .WithMany(b => b.Days)
                .UsingEntity<DaySubject>(
                    j => j
                        .HasOne(b => b.Subject)
                        .WithMany(b => b.DaysSubjects)
                        .HasForeignKey(b => b.SubjectId),
                    j => j
                        .HasOne(b => b.Day)
                        .WithMany(b => b.DaysSubjects)
                        .HasForeignKey(b => b.DayId));
        }
    }
}