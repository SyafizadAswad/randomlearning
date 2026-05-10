using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using EmployeesDataAccess;
using EmployeesDataAccess.Models;
using EmployeesAPI.Logic;
using EmployeesAPI.Model;
using EmployeesDataAccess.Interfaces;
using EmployeesAPI.Interfaces;

namespace EmployeesAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class EmployeesController : ControllerBase
    {
        private readonly IEmployeeLogic _employeeLogic;

        public EmployeesController(IEmployeeLogic employeeLogic)
        {
            _employeeLogic = employeeLogic;
        }

        // GET: api/Employees
        [HttpGet]
        public async Task<ActionResult<IEnumerable<EmployeeResponse>>> GetEmployee()
        {
            var employees = await _employeeLogic.GetAllEmployees();
            return Ok(employees);
        }

        // GET: api/Employee by id
        [HttpGet("{employeeNumber}")]
        public async Task<ActionResult<EmployeeResponse>> GetEmployee(string employeeNumber)
        {
            var employee = await _employeeLogic.GetEmployee(employeeNumber);
            return Ok(employee);
        }


        // POST: api/Employees
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Employee>> PostEmployee(EmployeeRequest request)
        {
            var response = await _employeeLogic.CreateEmployee(request);

            return CreatedAtAction(nameof(GetEmployee), new { id = response.EmployeeNumber }, response);
        }

        // PUT: api/Employee
        [HttpPut("{employeeNumber}")]
        public async Task<IActionResult> PutEmployee(string employeeNumber, EmployeeRequest request)
        {
            await _employeeLogic.EditEmployee(employeeNumber, request);
            return NoContent();
        }

        // DELETE: api/Employee
        [HttpDelete("{employeeNumber}")]
        public async Task<IActionResult> DeleteEmployee(string employeeNumber)
        {
            await _employeeLogic.DeleteEmployee(employeeNumber);
            return NoContent();
        }

    }
}
