from parser import parser

parser = parser()

parser.parse_chip( "2021-07-01", "2021-07-03" )

parser.parse_chip_indiv( 1103, "2021-07-01", "2021-07-03", None )

parser.parse_tech( 2330, "2021-05", "2021-08" )

parser.parse_revenue( "2021-01", "2021-03" )

parser.parse_revenue_indiv( 2330, "2021-01", "2021-03" )