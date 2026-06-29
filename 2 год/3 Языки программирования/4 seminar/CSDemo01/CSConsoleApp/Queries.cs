using System;
using System.Collections.Generic;
using System.Linq;

namespace CSConsoleApp;

internal static class Queries
{
    public static IEnumerable<MovieCredit> DirectedBy(this IEnumerable<MovieCredit> data, string directorName) =>
        data.Where(m => m.Crew.Any(c => c.Job == "Director" && c.Name == directorName));

    public static IEnumerable<string> CharactersOfActor(this IEnumerable<MovieCredit> data, string actorName) =>
        data.SelectMany(m => m.Cast.Where(c => c.Name == actorName).Select(c => c.Character))
            .Where(s => !string.IsNullOrWhiteSpace(s))
            .Distinct();

    public static IEnumerable<(MovieCredit Movie, int Count)> TopByCastSize(this IEnumerable<MovieCredit> data, int n) =>
        data.Select(m => (m, m.Cast.Count)).OrderByDescending(t => t.Item2).ThenBy(t => t.m.Title).Take(n);

    public static IEnumerable<(string Actor, int Movies)> TopActorsByMovies(this IEnumerable<MovieCredit> data, int n) =>
        data.SelectMany(m => m.Cast.Select(c => (c.Name, m.MovieId)))
            .Distinct()
            .GroupBy(x => x.Name)
            .Select(g => (Actor: g.Key, Movies: g.Count()))
            .OrderByDescending(x => x.Movies).ThenBy(x => x.Actor)
            .Take(n);

    public static IEnumerable<string> UniqueDepartments(this IEnumerable<MovieCredit> data) =>
        data.SelectMany(m => m.Crew.Select(c => c.Department))
            .Where(s => !string.IsNullOrWhiteSpace(s))
            .Distinct()
            .OrderBy(s => s);

    public static IEnumerable<MovieCredit> MoviesWithComposer(this IEnumerable<MovieCredit> data, string name) =>
        data.Where(m => m.Crew.Any(c => c.Job == "Original Music Composer" && c.Name == name));

    public static Dictionary<int, string> DirectorByMovieId(this IEnumerable<MovieCredit> data) =>
        data.ToDictionary(m => m.MovieId,
                          m => string.Join(", ", m.Crew.Where(c => c.Job == "Director")
                                                       .Select(c => c.Name).Distinct()));

    public static IEnumerable<MovieCredit> MoviesWithBothActors(this IEnumerable<MovieCredit> data, string a, string b) =>
        data.Where(m => {
            var names = m.Cast.Select(c => c.Name).ToHashSet(StringComparer.Ordinal);
            return names.Contains(a) && names.Contains(b);
        });

    public static int UniquePeopleInDepartment(this IEnumerable<MovieCredit> data, string department) =>
        data.SelectMany(m => m.Crew.Where(c => c.Department == department).Select(c => c.Name))
            .Where(n => !string.IsNullOrWhiteSpace(n))
            .Distinct(StringComparer.Ordinal).Count();

    public static IEnumerable<string> BothCastAndCrewInMovie(this IEnumerable<MovieCredit> data, string title) =>
        data.Where(m => string.Equals(m.Title, title, StringComparison.Ordinal))
            .SelectMany(m =>
            {
                var cast = m.Cast.Select(c => c.Name).ToHashSet(StringComparer.Ordinal);
                var crew = m.Crew.Select(c => c.Name).ToHashSet(StringComparer.Ordinal);
                cast.IntersectWith(crew);
                return cast;
            })
            .Distinct().OrderBy(n => n);

    public static IEnumerable<(string Person, int Movies)> InnerCircle(this IEnumerable<MovieCredit> data, string director, int topN) =>
        data.Where(m => m.Crew.Any(c => c.Job == "Director" && c.Name == director))
            .Select(m => (m.MovieId, m.Crew))
            .SelectMany(t => t.Crew.Select(c => (c.Name, t.MovieId)))
            .Where(x => x.Name != director)
            .Distinct()
            .GroupBy(x => x.Name)
            .Select(g => (Person: g.Key, Movies: g.Count()))
            .OrderByDescending(x => x.Movies).ThenBy(x => x.Person)
            .Take(topN);

    public static IEnumerable<((string A, string B) Pair, int Movies)> TopActorDuos(this IEnumerable<MovieCredit> data, int topN)
    {
        var counts = new Dictionary<(string, string), int>();
        foreach (var m in data)
        {
            var names = m.Cast.Select(c => c.Name).Where(s => !string.IsNullOrWhiteSpace(s))
                              .Distinct().OrderBy(s => s, StringComparer.Ordinal).ToArray();
            for (int i = 0; i < names.Length; i++)
                for (int j = i + 1; j < names.Length; j++)
                    counts[(names[i], names[j])] = counts.TryGetValue((names[i], names[j]), out var c) ? c + 1 : 1;
        }
        return counts.Select(kv => (Pair: kv.Key, Movies: kv.Value))
                     .OrderByDescending(x => x.Movies)
                     .ThenBy(x => x.Pair.Item1).ThenBy(x => x.Pair.Item2)
                     .Take(topN);
    }

    public static IEnumerable<(string Person, int DeptCount, string[] Depts)> DiversityIndex(this IEnumerable<MovieCredit> data, int topN) =>
        data.SelectMany(m => m.Crew.Select(c => (c.Name, c.Department)))
            .Where(x => !string.IsNullOrWhiteSpace(x.Name) && !string.IsNullOrWhiteSpace(x.Department))
            .GroupBy(x => x.Name)
            .Select(g => (Person: g.Key,
                          DeptCount: g.Select(x => x.Department).Distinct().Count(),
                          Depts: g.Select(x => x.Department).Distinct().OrderBy(d => d).ToArray()))
            .OrderByDescending(x => x.DeptCount).ThenBy(x => x.Person)
            .Take(topN);

    public static IEnumerable<(MovieCredit Movie, string Person)> CreativeTrios(this IEnumerable<MovieCredit> data)
    {
        static bool IsWriterJob(string job) =>
            job is "Writer" or "Screenplay" or "Author" or "Story" or "Characters";

        return data.Select(m =>
        {
            var byPerson = m.Crew.GroupBy(c => c.Name);
            foreach (var g in byPerson)
            {
                var jobs = g.Select(c => c.Job).ToHashSet(StringComparer.Ordinal);
                if (jobs.Contains("Director") && jobs.Any(IsWriterJob) && jobs.Any(j => j.Contains("Producer", StringComparison.Ordinal)))
                    return (Movie: m, Person: g.Key);
            }
            return (Movie: (MovieCredit)null!, Person: "");
        })
        .Where(t => t.Movie != null);
    }

    public static IEnumerable<string> TwoStepsTo(this IEnumerable<MovieCredit> data, string actor)
    {
        var co = BuildCoActorGraph(data);
        if (!co.TryGetValue(actor, out var direct)) return Array.Empty<string>();
        var result = new HashSet<string>(StringComparer.Ordinal);

        foreach (var n1 in direct)
        {
            if (!co.TryGetValue(n1, out var n2set)) continue;
            foreach (var n2 in n2set)
                if (n2 != actor && !direct.Contains(n2))
                    result.Add(n2);
        }
        return result.OrderBy(s => s);
    }

    public static IEnumerable<(string Director, double AvgCast, double AvgCrew)> Teamwork(this IEnumerable<MovieCredit> data)
    {
        var items = data.Select(m => new {
            m.Title,
            CastCount = m.Cast.Count,
            CrewCount = m.Crew.Count,
            Directors = m.Crew.Where(c => c.Job == "Director").Select(c => c.Name).Distinct()
        });

        return items.SelectMany(x => x.Directors.Select(d => (Director: d, x.CastCount, x.CrewCount)))
                    .GroupBy(x => x.Director)
                    .Select(g => (g.Key,
                                  AvgCast: g.Average(x => x.CastCount),
                                  AvgCrew: g.Average(x => x.CrewCount)))
                    .OrderBy(t => t.Key);
    }

    public static IEnumerable<(string Person, string Department, int Count)> MultiTalents(this IEnumerable<MovieCredit> data)
    {
        var actors = data.SelectMany(m => m.Cast.Select(c => c.Name)).Where(n => !string.IsNullOrWhiteSpace(n)).ToHashSet(StringComparer.Ordinal);
        var crew = data.SelectMany(m => m.Crew.Select(c => (c.Name, c.Department)))
                       .Where(t => !string.IsNullOrWhiteSpace(t.Name) && !string.IsNullOrWhiteSpace(t.Department));

        var byPerson = crew.GroupBy(x => x.Name);
        foreach (var g in byPerson)
        {
            if (!actors.Contains(g.Key)) continue;
            var best = g.GroupBy(x => x.Department)
                        .Select(gg => (Dept: gg.Key, Cnt: gg.Count()))
                        .OrderByDescending(t => t.Cnt).ThenBy(t => t.Dept)
                        .FirstOrDefault();
            if (best.Dept != null)
                yield return (g.Key, best.Dept, best.Cnt);
        }
    }

    public static IEnumerable<string> WorkedWithBoth(this IEnumerable<MovieCredit> data, string dirA, string dirB)
    {
        var moviesA = data.Where(m => m.Crew.Any(c => c.Job == "Director" && c.Name == dirA)).ToArray();
        var moviesB = data.Where(m => m.Crew.Any(c => c.Job == "Director" && c.Name == dirB)).ToArray();

        var setA = moviesA.SelectMany(m => m.Cast.Select(c => c.Name).Concat(m.Crew.Select(c => c.Name))).ToHashSet(StringComparer.Ordinal);
        var setB = moviesB.SelectMany(m => m.Cast.Select(c => c.Name).Concat(m.Crew.Select(c => c.Name))).ToHashSet(StringComparer.Ordinal);

        setA.IntersectWith(setB);
        return setA.OrderBy(n => n);
    }

    public static IEnumerable<(string Department, double AvgCast)> DepartmentInfluence(this IEnumerable<MovieCredit> data)
    {
        var byDept = data.SelectMany(m => m.Crew.Select(c => (m, c.Department)))
                         .Where(t => !string.IsNullOrWhiteSpace(t.Department))
                         .GroupBy(t => t.Department);

        return byDept.Select(g => (Department: g.Key,
                                   AvgCast: g.Select(x => x.m).Distinct()
                                             .Average(mm => (double)mm.Cast.Count)))
                     .OrderByDescending(t => t.AvgCast)
                     .ThenBy(t => t.Department);
    }

    public static IEnumerable<(string Archetype, int Count)> Archetypes(this IEnumerable<MovieCredit> data, string actor)
    {
        static string FirstWord(string? s)
        {
            if (string.IsNullOrWhiteSpace(s)) return "";
            var w = s.Trim();
            int space = w.IndexOf(' ');
            var first = space >= 0 ? w[..space] : w;
            return first.Trim('\"', '\'', '.', ',', '!', '?', ':', ';', '(', ')', '[', ']');
        }

        return data.SelectMany(m => m.Cast.Where(c => c.Name == actor).Select(c => FirstWord(c.Character)))
                   .Where(w => !string.IsNullOrWhiteSpace(w))
                   .GroupBy(w => w)
                   .Select(g => (g.Key, g.Count()))
                   .OrderByDescending(t => t.Item2).ThenBy(t => t.Key);
    }

    public static void ExecuteAll(IReadOnlyList<MovieCredit> movieCredits)
    {
        PrintHeader("Фильмы, снятые Steven Spielberg");
        foreach (var i in movieCredits.DirectedBy("Steven Spielberg"))
            Console.WriteLine(i.Title);

        PrintHeader("Персонажи Tom Hanks");
        foreach (var i in movieCredits.CharactersOfActor("Tom Hanks"))
            Console.WriteLine(i);

        PrintHeader("Топ-5 фильмов по количеству актёров");
        foreach (var i in movieCredits.TopByCastSize(5))
            Console.WriteLine($"{i.Movie.Title} — {i.Count}");

        PrintHeader("Топ-10 актёров по числу фильмов");
        foreach (var i in movieCredits.TopActorsByMovies(10))
            Console.WriteLine($"{i.Actor} — {i.Movies}");

        PrintHeader("Уникальные департаменты съёмочной группы");
        foreach (var i in movieCredits.UniqueDepartments())
            Console.WriteLine(i);

        PrintHeader("Фильмы с композитором Hans Zimmer");
        foreach (var i in movieCredits.MoviesWithComposer("Hans Zimmer"))
            Console.WriteLine(i.Title);

        PrintHeader("Словарь: MovieID -> Director(s)");
        var dict = movieCredits.DirectorByMovieId();
        foreach (var i in dict.Take(30))
            Console.WriteLine($"{i.Key} -> {i.Value}");
        Console.WriteLine($"... всего {dict.Count} фильмов");

        PrintHeader("Фильмы с Brad Pitt и George Clooney");
        foreach (var i in movieCredits.MoviesWithBothActors("Brad Pitt", "George Clooney"))
            Console.WriteLine(i.Title);

        PrintHeader("Сколько людей в департаменте Camera (уникальные)");
        Console.WriteLine(movieCredits.UniquePeopleInDepartment("Camera"));

        PrintHeader("В Titanic одновременно и актёры, и члены группы");
        foreach (var i in movieCredits.BothCastAndCrewInMovie("Titanic"))
            Console.WriteLine(i);

        PrintHeader("«Внутренний круг» Quentin Tarantino (топ-5)");
        foreach (var i in movieCredits.InnerCircle("Quentin Tarantino", 5))
            Console.WriteLine($"{i.Person} — {i.Movies}");

        PrintHeader("Топ-10 актёрских дуэтов");
        foreach (var i in movieCredits.TopActorDuos(10))
            Console.WriteLine($"{i.Pair.A} + {i.Pair.B} — {i.Movies}");

        PrintHeader("Индекс разнообразия карьеры (топ-5)");
        foreach (var i in movieCredits.DiversityIndex(5))
            Console.WriteLine($"{i.Person} — {i.DeptCount}: {string.Join(", ", i.Depts)}");

        PrintHeader("Творческие «трио»: Director & Writer & Producer — в одном лице");
        foreach (var i in movieCredits.CreativeTrios())
            Console.WriteLine($"{i.Movie.Title} — {i.Person}");

        PrintHeader("Два шага до Kevin Bacon");
        foreach (var i in movieCredits.TwoStepsTo("Kevin Bacon").Take(200))
            Console.WriteLine(i);

        PrintHeader("Командная работа: средний Cast/Crew по режиссёрам");
        foreach (var i in movieCredits.Teamwork())
            Console.WriteLine($"{i.Director} — AvgCast: {i.AvgCast:F2}, AvgCrew: {i.AvgCrew:F2}");

        PrintHeader("Универсалы: чаще всего работали в департаменте");
        foreach (var i in movieCredits.MultiTalents().OrderBy(i => i.Person).Take(200))
            Console.WriteLine($"{i.Person} — {i.Department} ({i.Count})");

        PrintHeader("Работали и со Scorsese, и с Christopher Nolan");
        foreach (var i in movieCredits.WorkedWithBoth("Martin Scorsese", "Christopher Nolan"))
            Console.WriteLine(i);

        PrintHeader("Скрытое влияние департаментов (AvgCast)");
        foreach (var i in movieCredits.DepartmentInfluence().Take(50))
            Console.WriteLine($"{i.Department} — AvgCast: {i.AvgCast:F2}");

        PrintHeader("Архетипы персонажей: Johnny Depp (первое слово роли)");
        foreach (var i in movieCredits.Archetypes("Johnny Depp"))
            Console.WriteLine($"{i.Archetype} — {i.Count}");
    }

    private static void PrintHeader(string title)
    {
        Console.WriteLine();
        Console.WriteLine(new string('─', Math.Max(8, title.Length)));
        Console.WriteLine(title);
        Console.WriteLine(new string('─', Math.Max(8, title.Length)));
    }

    private static Dictionary<string, HashSet<string>> BuildCoActorGraph(IEnumerable<MovieCredit> data)
    {
        var g = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);
        foreach (var m in data)
        {
            var names = m.Cast.Select(c => c.Name).Where(s => !string.IsNullOrWhiteSpace(s)).Distinct().ToArray();
            foreach (var a in names)
            {
                if (!g.TryGetValue(a, out var set)) g[a] = set = new HashSet<string>(StringComparer.Ordinal);
                foreach (var b in names)
                    if (b != a) set.Add(b);
            }
        }
        return g;
    }
}
