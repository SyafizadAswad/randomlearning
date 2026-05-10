using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using EmployeesDataAccess.Models;

namespace EmployeesDataAccess.Interfaces
{
    public interface IEmployeeRepository
    {
        Task<IEnumerable<Employee>> GetAllEmployeesAsync();
        Task<Employee?> GetEmployeeAsync(string employeeNumber);
        Task<Employee> AddEmployeeAsync(Employee employee);
        Task EditEmployeeAsync(Employee employee);
        Task DeleteEmployeeAsync(Employee employee);
        Task<bool> ExistAsync(string employeeNumber);
    }
}
