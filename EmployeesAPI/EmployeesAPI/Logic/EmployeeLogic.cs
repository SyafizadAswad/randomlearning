using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using EmployeesDataAccess;
using EmployeesDataAccess.Models;
using EmployeesAPI.Model;
using EmployeesDataAccess.Repositories;
using EmployeesDataAccess.Interfaces;
using EmployeesAPI.Interfaces;
using EmployeesAPI.Exceptions;

namespace EmployeesAPI.Logic
{
    public class EmployeeLogic : IEmployeeLogic
    {
        private readonly IEmployeeRepository _employeeRepository;

        public EmployeeLogic(IEmployeeRepository employeeRepository)
        {
            _employeeRepository = employeeRepository;
        }

        // GET
        public async Task<IEnumerable<EmployeeResponse>> GetAllEmployees()
        {
            var employees = await _employeeRepository.GetAllEmployeesAsync();

            // map the list of entities to a list of response DTO
            return employees.Select(e => new EmployeeResponse
            {
                EmployeeNumber = e.EmployeeNumber,
                EmployeeName = e.EmployeeName,
                JoinDate = e.JoinDate,
                DepartmentId = e.DepartmentId ?? 0,
                // combined part - accessing the joined dept table property
                DeparmentName = e.Department?.DepartmentName ?? "No Department",
                MailAddress = e.MailAddress
            });
        }

        // GET by id
        public async Task<EmployeeResponse> GetEmployee(string employeeNumber)
        {
            var employee = await _employeeRepository.GetEmployeeAsync(employeeNumber);

            if (employee == null) throw new NotFoundException("Employee does not exist");

            return new EmployeeResponse
            {
                EmployeeNumber = employee.EmployeeNumber,
                EmployeeName = employee.EmployeeName,
            };
        }


        // POST
        public async Task<EmployeeResponse> CreateEmployee(EmployeeRequest request)
        {
            // check for dupes
            if (await _employeeRepository.ExistAsync(request.EmployeeNumber))
            {
                // throw conflict exception, which middleware will catch
                throw new ConflictException("Employee number already exist");
            }

            // map request to DTO to Entity
            var employee = new Employee
            {
                EmployeeNumber = request.EmployeeNumber,
                EmployeeName = request.EmployeeName,
                JoinDate = request.JoinDate == default ? DateTime.Now : request.JoinDate,
                DepartmentId = request.DepartmentId,
                MailAddress = request.MailAddress
            };

            // call repo to save
            var savedEmployee = await _employeeRepository.AddEmployeeAsync(employee);

            // map entity back to resnponse DTO
            return new EmployeeResponse { };
        }

        // PUT
        public async Task EditEmployee(string employeeNumber, EmployeeRequest request)
        {
            var existingEmployee = await _employeeRepository.GetEmployeeAsync(employeeNumber);

            if (existingEmployee == null) throw new NotFoundException($"Employee {employeeNumber} does not exist");

            existingEmployee.EmployeeName = request.EmployeeName;
            existingEmployee.JoinDate = request.JoinDate;
            existingEmployee.DepartmentId = request.DepartmentId;
            existingEmployee.MailAddress = request.MailAddress;

            await _employeeRepository.EditEmployeeAsync(existingEmployee);

        }

        // DELETE
        public async Task DeleteEmployee(string employeeNumber)
        {
            var employee = await _employeeRepository.GetEmployeeAsync(employeeNumber);

            if (employee == null) throw new NotFoundException($"Employee {employeeNumber} doesn not exist");

            _employeeRepository.DeleteEmployeeAsync(employee);
        }

        private async Task<bool> IsEmployeeDuplicateAsync(EmployeeRequest request)
        {
            // call repo method, passing only ID and not the whole request
            return await _employeeRepository.ExistAsync(request.EmployeeNumber);
        }
    }
}
