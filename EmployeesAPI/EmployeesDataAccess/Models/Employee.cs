using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EmployeesDataAccess.Models
{
    [Table("Employees")]
    public class Employee
    {
        [Key]
        [Required]
        public string EmployeeNumber { get; set; }

        [Required]
        public string EmployeeName { get; set; }

        [Required]
        public DateTime JoinDate { get; set; }
        public int? DepartmentId { get; set; }

        [ForeignKey("DepartmentId")]
        public virtual Department? Department { get; set; }

        public string? MailAddress { get; set; }
    }
}
