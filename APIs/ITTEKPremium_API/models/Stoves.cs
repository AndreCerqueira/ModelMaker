using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ITTEKPremium_API.Models
{
	public class Stoves 
	{
		[Key]
		public int id { get; set; }

		public int stove_number { get; set; }

		public bool active { get; set; }

	}
}