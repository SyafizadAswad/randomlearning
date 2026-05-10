using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using EmployeesAPI.Model;
using Microsoft.AspNetCore.Mvc;

namespace EmployeesAPI.Interfaces
{
    public interface IEmployeeLogic
    {
        Task<IEnumerable<EmployeeResponse>> GetAllEmployees();

        Task<EmployeeResponse?> GetEmployee(string employeeNumber);

        Task<EmployeeResponse> CreateEmployee(EmployeeRequest request);

        Task EditEmployee(string employeeNumber, EmployeeRequest request);

        Task DeleteEmployee(string employeeNumber);

    }
}
