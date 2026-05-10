using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using EmployeesDataAccess.Models;
using EmployeesDataAccess.Interfaces;

namespace EmployeesDataAccess.Repositories
{
    public class EmployeeRepository : IEmployeeRepository
    {
        private readonly DataAccessContext _context;

        public EmployeeRepository(DataAccessContext context)
        {
            _context = context;
        }

        // GET
        public async Task<IEnumerable<Employee>> GetAllEmployeesAsync()
        {
            // use include if need to bring in dept data for frontend
            return await _context.Employee
                .Include(e => e.Department)  // attach dept table?
                .ToListAsync();
        }

        // GET by id
        public async Task<Employee> GetEmployeeAsync(string employeeNumber)
        {
            return await _context.Employee.FirstOrDefaultAsync(e => e.EmployeeNumber == employeeNumber);

        }

        // POST
        public async Task<Employee> AddEmployeeAsync(Employee employee)
        {
            await _context.Employee.AddAsync(employee);
            await _context.SaveChangesAsync();
            return employee;
        }

        // PUT
        public async Task EditEmployeeAsync(Employee employee)
        {
            _context.Entry(employee).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        // DELETE
        public async Task DeleteEmployeeAsync(Employee employee)
        {
            _context.Employee.Remove(employee);
            await _context.SaveChangesAsync();
        }

        public async Task<bool> ExistAsync(string employeeNumber)
        {
            return await _context.Employee.AnyAsync(e => e.EmployeeNumber == employeeNumber);
        }

    }
}
