from gemini.api import Trait
import pandas as pd

trait = Trait(trait_name="Average Temperature")

trait_records = trait.get_records()
trait_records_df = pd.DataFrame(trait_records)
print(trait_records_df)