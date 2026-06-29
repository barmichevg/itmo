using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text.Json;
using System.Collections.Generic;
using System.Text;

namespace CSConsoleApp;

internal static class CreditsCsvLoader
{

    private static class Csv
    {
        public static List<string> SplitLine(string line)
        {
            var res = new List<string>();
            var sb = new StringBuilder();
            bool inQuotes = false;

            for (int i = 0; i < line.Length; i++)
            {
                char c = line[i];
                if (c == '"')
                {
                    if (inQuotes && i + 1 < line.Length && line[i + 1] == '"')
                    {
                        sb.Append('"');
                        i++;
                    }
                    else
                    {
                        inQuotes = !inQuotes;
                    }
                }
                else if (c == ',' && !inQuotes)
                {
                    res.Add(sb.ToString());
                    sb.Clear();
                }
                else
                {
                    sb.Append(c);
                }
            }
            res.Add(sb.ToString());
            return res;
        }
    }

    private sealed class CastDto
    {
        public int cast_id { get; set; }
        public string character { get; set; } = "";
        public string credit_id { get; set; } = "";
        public int gender { get; set; }
        public int id { get; set; }
        public string name { get; set; } = "";
        public int order { get; set; }
    }

    private sealed class CrewDto
    {
        public string credit_id { get; set; } = "";
        public string department { get; set; } = "";
        public int gender { get; set; }
        public int id { get; set; }
        public string job { get; set; } = "";
        public string name { get; set; } = "";
    }

    public static IReadOnlyList<MovieCredit> Load(string path)
    {
        var opts = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        var list = new List<MovieCredit>(5500);

        using var sr = new StreamReader(path);
        _ = sr.ReadLine();

        while (true)
        {
            var line = sr.ReadLine();
            if (line == null) break;
            if (line.Length == 0) continue;

            var fields = Csv.SplitLine(line);
            if (fields.Count < 4) continue;

            int movieId = int.TryParse(fields[0], NumberStyles.Integer, CultureInfo.InvariantCulture, out var mid) ? mid : 0;
            string title = fields[1];

            var cast = new List<CastMember>();
            var crew = new List<CrewMember>();

            // CAST
            try
            {
                var castArr = JsonSerializer.Deserialize<List<CastDto>>(fields[2], opts) ?? new();
                foreach (var c in castArr)
                {
                    cast.Add(new CastMember(
                        c.cast_id,
                        c.character ?? "",
                        c.credit_id ?? "",
                        c.gender,
                        c.id,
                        c.name ?? "",
                        c.order
                    ));
                }
            }
            catch { /* пропускаем битую строку cast */ }

            // CREW
            try
            {
                var crewArr = JsonSerializer.Deserialize<List<CrewDto>>(fields[3], opts) ?? new();
                foreach (var c in crewArr)
                {
                    crew.Add(new CrewMember(
                        c.credit_id ?? "",
                        c.department ?? "",
                        c.gender,
                        c.id,
                        c.job ?? "",
                        c.name ?? ""
                    ));
                }
            }
            catch { /* пропускаем битую строку crew */ }

            list.Add(new MovieCredit { MovieId = movieId, Title = title, Cast = cast, Crew = crew });
        }

        return list;
    }
}

