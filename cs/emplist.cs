namespace Kenshuu5
{
    class Program
    {
        public static void Main(string[] args)
        {

            string filePath = "employees.txt";

            Console.WriteLine("--- Employee Data Logger ---");

            bool keepRunning = true;
            while (keepRunning)
            {
                // input employee number
                Console.Write("\nEnter Employee Number: ");
                string? empNumber = Console.ReadLine();

                // input employee name
                Console.Write("Enter Employee Name: ");
                string? empName = Console.ReadLine();

                // append to file (creates if file not exist)
                try
                {
                    string record = $"ID: {empNumber} | Name: {empName} | Date Added: {DateTime.Now}";
                    File.AppendAllLines(filePath, [record]);
                    Console.WriteLine("Successfully saved to file.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error saving data: {ex.Message}");
                }

                // menu loop w/ failsafe logic
                bool validChoice = false;
                while (!validChoice)
                {
                    Console.WriteLine("\nChoose an option:");
                    Console.WriteLine("(1) Exit Program");
                    Console.WriteLine("(2) Add Another Entry");
                    Console.Write("Selection: ");

                    string? input = Console.ReadLine();

                    if (input == "1")
                    {
                        keepRunning = false;
                        validChoice = true;
                        Console.WriteLine("Exiting... Goodbye!");
                    }
                    else if (input == "2")
                    {
                        validChoice = true;
                        Console.WriteLine("Continuing...");
                    }
                    else
                    {
                        Console.WriteLine("Invalid input. Please enter 1 or 2.");
                    }
                }
            }
        }
    }
}