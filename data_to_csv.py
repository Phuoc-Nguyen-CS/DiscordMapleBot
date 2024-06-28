import csv

data = """
200 > 201	2,207,026,470	286.4%
201 > 202	2,471,869,646	12%
202 > 203	2,768,494,003	12%
203 > 204	3,100,713,283	12%
204 > 205	3,472,798,876	12%
205 > 206	3,889,534,741	12%
206 > 207	4,356,278,909	12%
207 > 208	4,879,032,378	12%
208 > 209	5,464,516,263	12%
209 > 210	6,120,258,214	12%
210 > 211	7,956,335,678	30%
211 > 212	8,831,532,602	11%
212 > 213	9,803,001,188	11%
213 > 214	10,881,331,318	11%
214 > 215	12,078,277,762	11%
215 > 216	15,701,761,090	30%
216 > 217	17,114,919,588	9%
217 > 218	18,655,262,350	9%
218 > 219	20,334,235,961	9%
219 > 220	22,164,317,197	9%
220 > 221	28,813,612,356	30%
221 > 222	30,830,565,220	7%
222 > 223	32,988,704,785	7%
223 > 224	35,297,914,119	7%
224 > 225	37,768,768,107	7%
225 > 226	49,099,398,539	30%
226 > 227	52,536,356,436	7%
227 > 228	56,213,901,386	7%
228 > 229	60,148,874,483	7%
229 > 230	64,359,295,696	7%
230 > 231	83,667,084,404	30%
231 > 232	86,177,096,936	3%
232 > 233	88,762,409,844	3%
233 > 234	91,425,282,139	3%
234 > 235	94,168,040,603	3%
235 > 236	122,418,452,783	30%
236 > 237	126,091,006,366	3%
237 > 238	129,873,736,556	3%
238 > 239	133,769,948,652	3%
239 > 240	137,783,047,111	3%
240 > 241	179,117,961,244	30%
241 > 242	184,491,500,081	3%
242 > 243	190,026,245,083	3%
243 > 244	195,727,032,435	3%
244 > 245	201,598,843,408	3%
245 > 246	262,078,496,430	30%
246 > 247	269,940,851,322	3%
247 > 248	278,039,076,861	3%
248 > 249	286,380,249,166	3%
249 > 250	294,971,656,640	3%
250 > 251	442,457,484,960	50%
251 > 252	455,731,209,508	3%
252 > 253	469,403,145,793	3%
253 > 254	483,485,240,166	3%
254 > 255	497,989,797,370	3%
255 > 256	512,929,491,291	3%
256 > 257	528,317,376,029	3%
257 > 258	544,166,897,309	3%
258 > 259	560,491,904,228	3%
259 > 260	577,306,661,354	3%
260 > 261	1,731,919,984,062	200%
261 > 262	1,749,239,183,902	1%
262 > 263	1,766,731,575,741	1%
263 > 264	1,784,398,891,498	1%
264 > 265	1,802,242,880,412	1%
265 > 266	2,342,915,744,535	30%
266 > 267	2,366,344,901,980	1%
267 > 268	2,390,008,350,999	1%
268 > 269	2,413,908,434,508	1%
269 > 270	2,438,047,518,853	1%
270 > 271	5,412,465,491,851	122%
271 > 272	5,466,590,146,770	1%
272 > 273	5,521,256,048,237	1%
273 > 274	5,576,468,608,720	1%
274 > 275	5,632,233,294,807	1%
275 > 276	11,377,111,255,510	102%
276 > 277	12,514,822,381,061	10%
277 > 278	13,766,304,619,167	10%
278 > 279	15,142,935,081,084	10%
279 > 280	16,657,228,589,191	10%
280 > 281	33,647,601,750,165	102%
281 > 282	37,012,361,925,183	10%
282 > 283	40,713,598,117,701	10%
283 > 284	44,784,957,929,471	10%
284 > 285	49,263,453,722,418	10%
285 > 286	99,512,176,519,285	102%
286 > 287	109,463,394,171,214	10%
287 > 288	120,409,733,588,335	10%
288 > 289	132,450,706,947,169	10%
289 > 290	145,695,777,641,885	10%
290 > 291	294,305,470,836,608	102%
291 > 292	323,736,017,920,269	10%
292 > 293	356,109,619,712,296	10%
293 > 294	391,720,581,683,526	10%
294 > 295	430,892,639,851,879	10%
295 > 296	870,403,132,500,795	102%
296 > 297	957,443,445,750,874	10%
297 > 298	1,053,187,790,325,960	10%
298 > 299	1,158,506,569,358,560	10%
299 > 300	1,737,759,854,037,840	50%
""".strip().split('\n')

# Split each line into a list of values
data = [line.split('\t') for line in data]

# Write data to CSV file
with open('level_exp.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Level", "EXP to Next Level"])  # Write header
    for line in data:
        level_range, exp, _ = line
        level = level_range.split(' > ')[0]  # Extract the start level
        exp = exp.replace(',', '')  # Remove commas from EXP values
        writer.writerow([level, exp])
