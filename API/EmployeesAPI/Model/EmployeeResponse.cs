namespace EmployeesAPI.Model
{
    public class EmployeeResponse
    {
        public string EmployeeNumber { get; set; }
        public string EmployeeName { get; set; }
        public DateTime JoinDate { get; set; }
        public int DepartmentId { get; set; }
        public string DeparmentName { get; set; }
        public string MailAddress { get; set; }

        // for angular UI
        public string JoinDateDisplay => JoinDate.ToString("yyyy-MM-dd");


    }
}
