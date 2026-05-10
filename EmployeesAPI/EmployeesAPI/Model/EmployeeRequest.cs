using System.ComponentModel.DataAnnotations;

namespace EmployeesAPI.Model
{
    public class EmployeeRequest
    {
        [Required]
        [StringLength(7)]
        public string EmployeeNumber { get; set; }

        [Required]
        [StringLength(100)]
        public string EmployeeName { get; set; }

        [Required]
        public DateTime JoinDate { get; set; } = DateTime.Now;

        public int DepartmentId { get; set; }
        public string MailAddress { get; set; }
    }
}
