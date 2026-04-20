namespace Kenshuu5
{
    class Program
    {
        public static void Main(string[] args)
        {

            string filePath = "employees.txt";

            // Check if the file exists before starting
            if (!File.Exists(filePath))
            {
                Console.WriteLine("Error: The file 'employees.txt' was not found. Please add data first.");
                return;
            }

            bool keepRunning = true;
            while (keepRunning)
            {
                Console.WriteLine("\n--- Employee Records Viewer ---");
                Console.WriteLine("1. Output All Records");
                Console.WriteLine("2. Search by Employee Number");
                Console.WriteLine("3. Search by Employee Name");
                Console.WriteLine("4. Exit");
                Console.Write("Select an option: ");

                string? choice = Console.ReadLine();
                string[] lines = File.ReadAllLines(filePath);

                switch (choice)
                {
                    case "1":
                        DisplayAll(lines);
                        break;
                    case "2":
                        SearchRecord(lines, "ID:");
                        break;
                    case "3":
                        SearchRecord(lines, "Name:");
                        break;
                    case "4":
                        keepRunning = false;
                        Console.WriteLine("Closing viewer...");
                        break;
                    default:
                        Console.WriteLine("Invalid selection. Please choose 1, 2, 3, or 4.");
                        break;
                }
            }

            // --- Functions ---

            void DisplayAll(string[] records)
            {
                Console.WriteLine("\n--- All Records ---");
                if (records.Length == 0) Console.WriteLine("File is empty.");
                foreach (string line in records)
                {
                    Console.WriteLine(line);
                }
            }

            void SearchRecord(string[] records, string prefix)
            {
                Console.Write($"Enter {prefix.Replace(":", "")} to search: ");
                string? query = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(query))
                {
                    Console.WriteLine("Search term cannot be empty.");
                    return;
                }

                // filter lines that contain both the label (ID or Name) and the user's query
                var results = records.Where(line => line.Contains($"{prefix} {query}", StringComparison.OrdinalIgnoreCase)).ToList();

                if (results.Any())
                {
                    Console.WriteLine("\n--- Search Results ---");
                    foreach (var result in results)
                    {
                        Console.WriteLine(result);
                    }
                }
                else
                {
                    Console.WriteLine($"\n[!] No records found matching: {query}");
                }
            }
        }
    }
}