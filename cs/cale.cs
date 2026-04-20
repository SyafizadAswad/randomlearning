namespace Kenshuu4
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("年月を入力してください（例： 202604）:");
            string input = Console.ReadLine() ?? "";

            // extract year and month from input string
            if (input.Length == 6 && int.TryParse(input.Substring(0, 4), out int year)
                                 && int.TryParse(input.Substring(4, 2), out int month))
            {
                // exits program if invalid month entered
                if (month < 1 || month > 12)
                {
                    Console.WriteLine("月が存在しません");
                    return;
                }

                string[,] calendar = CreateCalendar(year, month);
                DisplayCalendar(calendar, year, month);
            }
            else
            {
                Console.WriteLine("Invalid format. Please use YYYYMM.");
            }
        }

        static string[,] CreateCalendar(int year, int month)
        {
            // create 6x7 grid (calendar template)
            string[,] calendar = new string[6, 7];

            int daysInMonth = GetDaysInMonth(year, month);
            int startDay = GetFirstDayOfMonth(year, month); // 0 = Sunday, 1 = Monday...

            int currentColumn = startDay;
            int currentRow = 0;

            // main calendar layour loop
            // increment day till end of month
            for (int day = 1; day <= daysInMonth; day++)
            {
                calendar[currentRow, currentColumn] = day.ToString().PadLeft(2);
                currentColumn++;

                // if current column at the end of row, wrap and go down
                if (currentColumn > 6)
                {
                    currentColumn = 0;
                    currentRow++;
                }
            }

            return calendar;
        }

        // get number of days in month
        static int GetDaysInMonth(int year, int month)
        {
            if (month == 2)
            {
                // check leap year - divisible by 4 but not 100, OR divisible by 400
                bool isLeap = (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
                // terniary operator - 29 if leap, else 28 
                return isLeap ? 29 : 28;
            }

            // months with 30 days: 4/6/9/11
            if (month == 4 || month == 6 || month == 9 || month == 11)
                return 30;

            // else return with 31 days 
            return 31;
        }

        // datetime function to get 1st day of month
        static int GetFirstDayOfMonth(int year, int month)
        {
            DateTime firstDay = new DateTime(year, month, 1);
            // 0 = 日, 1 = 月, 2 = 火, 3 = 水, 4 = 木, 5 = 金, 6 = 土
            return (int)firstDay.DayOfWeek; 
        }

        static void DisplayCalendar(string[,] calendar, int year, int month)
        {
            //string[] monthNames = { "", "January", "February", "March", "April", "May", "June",
            //                        "July", "August", "September", "October", "November", "December" };

            //Console.WriteLine($"\n--- {monthNames[month]} {year} ---");
            //Console.WriteLine(" Su  Mo  Tu  We  Th  Fr  Sa");

            // loops 6 times since array has 6 rows
            // hasData check if the row has date or not
            for (int r = 0; r < 6; r++)
            {
                string rowString = "";
                bool hasData = false;
                // Sun -> Sat loop
                for (int c = 0; c < 7; c++)
                {
                    // add a space, insert date. If empty, add 2 spaces (to avoid null)
                    rowString += $" {(calendar[r, c] ?? "  ")} ";
                    if (calendar[r, c] != null) hasData = true;
                }
                if (hasData) Console.WriteLine(rowString);
            }
        }
    }
}