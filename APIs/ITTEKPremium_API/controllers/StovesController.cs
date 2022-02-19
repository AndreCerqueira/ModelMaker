using ITTEKPremium_API.Context;
using ITTEKPremium_API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ITTEKPremium_API.Controllers
{
	[Route("api/")]
	[ApiController]
	public class StovesController : Controller 
	{
		
		//GET ALL
		[HttpGet]
		[Route("[controller]")]
		public async Task<ActionResult<List<Stoves>>> Get([FromServices] ITTEKNeivacorDevDbContext context)
		{
			var allStoves = await context.Stoves.FromSqlRaw("SELECT * FROM Stoves;").ToListAsync();
			return allStoves.ToList();
		}


		//GET BY ID
		[HttpGet]
		[Route("[controller]/{id:int}")]
		public async Task<ActionResult<List<Stoves>>> GetById([FromServices] ITTEKNeivacorDevDbContext context, int id)
		{
			var StovesId = await context.Stoves.FromSqlRaw("SELECT * FROM Stoves; WHERE ID="+ id).ToListAsync();
			return StovesId;
		}


		//POST
		[HttpPost]
		[Route("[controller]")]
		public async Task<ActionResult<Stoves>> Post([FromServices] ITTEKNeivacorDevDbContext context, [FromBody] Stoves model) 
		{
			if (ModelState.IsValid) 
			{
				context.Stoves.Add(model);
				await context.SaveChangesAsync();
				return model; 
			}
			else 
			{
				 return BadRequest(ModelState); 
			} 
		}


		//PUT
		[HttpPut("[controller]/{id}")]
		public async Task<ActionResult<Stoves>> Put([FromServices] ITTEKNeivacorDevDbContext context, [FromBody] Stoves model, int id)
		{
			try
			{
				if (ModelState.IsValid)
				{
					var entity = context.Stoves.FirstOrDefault(e => e.id == id);
					if (entity == null)
					{
						return BadRequest(ModelState);
					}
					else
					{
						entity.id = model.id;
						entity.stove_number = model.stove_number;
						entity.active = model.active;

						await context.SaveChangesAsync();
						return model;
					}
				}
				else
				{
					return BadRequest(ModelState);
				}
			}
			catch (Exception ex)
			{
				return BadRequest(ModelState);
			}
		}


		//DELETE
		[HttpDelete("[controller]/{id}")]
		public void Delete(int id)
		{
		}
	}
}